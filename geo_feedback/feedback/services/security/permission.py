# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from invenio_records_permissions.generators import SystemProcess
from invenio_records_permissions.policies.records import RecordPermissionPolicy

from invenio_records_permissions.generators import AuthenticatedUser

from geo_config.security.generators import GeoSecretariat
from geo_feedback.feedback.services.security.generators import IfDenied, FeedbackOwner


class FeedbackPermissionPolicy(RecordPermissionPolicy):
    """Feedback permission policy."""

    #
    # High-level permissions
    #
    can_use = [
        IfDenied(
            then_=[GeoSecretariat(), FeedbackOwner()],
            else_=[AuthenticatedUser()],
        ),
    ]

    can_curate = [GeoSecretariat(), SystemProcess()]

    can_manage = can_curate + [FeedbackOwner()]

    #
    # User rating permissions
    #

    # Allow record search
    can_search = can_use

    # Allow reading record metadata
    can_read = can_use

    # Allow submitting new record
    can_create = can_use

    # Allow editing published ratings
    can_update = can_manage

    # Allow deleting
    can_delete = can_manage

    # Allow approving/denying comments
    can_change_state = can_curate
