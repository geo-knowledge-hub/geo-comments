# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marketplace Items feedback service tasks."""

from celery import shared_task
from geo_rdm_records.proxies import current_marketplace_service

from geo_comments.comments.services.notification import notify_comments
from geo_comments.proxies import current_comments


@shared_task
def send_notification_email():
    """Send background email."""
    record_service = current_marketplace_service
    comment_service = current_comments.package_feedback_service

    notify_comments(
        record_service, comment_service, "marketplace-item", "feedback message"
    )
