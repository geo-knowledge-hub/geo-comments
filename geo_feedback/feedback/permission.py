# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#


from .generators import GeoSecretariat, FeedbackOwner

from invenio_records_permissions.generators import SystemProcess, AuthenticatedUser
from invenio_records_permissions.policies.records import RecordPermissionPolicy


class RecordRatingPermissionPolicy(RecordPermissionPolicy):
    """Access control configuration for Record ratings.
    """

    #
    # High-level permissions
    #
    can_use = [AuthenticatedUser()]
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
    can_edit = can_manage

    # Allow deleting
    can_delete = can_manage

    # Allow approving/denying comments
    can_change_state = can_curate


__all__ = (
    "RecordRatingPermissionPolicy"
)
