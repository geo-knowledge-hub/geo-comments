# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Notification functions."""

import arrow
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_mail.api import TemplatedMessage
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_users_resources.proxies import current_users_service
from sqlalchemy.exc import NoResultFound


def notify_comments(
    record_service,
    comment_service,
    notification_type,
    notification_template="geo_comments/email/notification.html",
):
    """Notify owners about new comments in their records.

    Note:
        This function is intended to be used as part of a Celery Task
        to avoid scalability problems.
    """
    utcnow = arrow.utcnow()

    # Defining the interval to get the updated records.
    # The strategy used here is to check new messages every hour.
    # Additionally, to avoid errors, we have added an overlap time
    # (= 5 minutes). This way, if a user registers a new comment at
    # the same time the worker notify, this message will not be excluded
    # in future interactions.
    start = utcnow.shift(hours=-1, minutes=-5)
    end = utcnow.shift(minutes=5)

    # Formatting
    start = start.format("YYYY-MM-DDTHH:mm")
    end = end.format("YYYY-MM-DDTHH:mm")

    # Defining the query to get the most recent comments
    interval = f"{start} TO {end}"

    # We are using the `updated` field to enable the system to send a new
    # notification to users in each update in the comment. For example,
    # if a user creates a comment and, after two hours, updates it. In this case,
    # the authors will be notified twice.
    query = f"updated:[{interval}]"

    # Searching for new comments
    res = comment_service.scan(system_identity, q=query)
    res = res.to_dict()

    comments = res["hits"]["hits"]

    # Filtering the owners email
    processed_records = []
    record_owners_email = []

    for comment in comments:
        # Avoiding sending many emails to the same
        # record owners.
        if comment["record"] in processed_records:
            continue

        # Retrieving the record owners
        try:
            record_metadata = record_service.read(system_identity, comment["record"])
            record_metadata = record_metadata.to_dict()

            record_owners = record_metadata["parent"]["access"]["owned_by"]
        except (PIDDoesNotExistError, NoResultFound):
            # ToDo: This is not the final solution! This is a temporary one,
            #       which we need to handle multiple types of data.
            continue

        # Retrieving the owners profile
        for record_owner in record_owners:
            if "user" in record_owner:
                owner_profile = current_users_service.read(
                    system_identity, record_owner["user"]
                )
                owner_profile = owner_profile.to_dict()

                # Checking if user can receive emails. To receive an email, user
                # must have the following properties:
                #   1. Must be `Active`;
                #   2. Must have `Email visibility` defined to `True`;
                #   3. Must have `Email` confirmed.
                is_active = owner_profile["active"]
                is_email_visible = (
                    owner_profile["preferences"]["email_visibility"] == "public"
                )
                is_email_confirmed = owner_profile["confirmed"]

                can_receive_email = (
                    is_active and is_email_visible and is_email_confirmed
                )

                if can_receive_email:
                    record_owners_email.append(owner_profile["email"])

        # Saving the reference to the record
        processed_records.append(comment["record"])

        if record_owners_email:
            # Preparing notification
            message = TemplatedMessage(
                template_html=notification_template,
                recipients=record_owners_email,
                ctx=dict(record=record_metadata, notification_type=notification_type),
            )

            # Sending notification
            current_app.extensions["mail"].send(message)
