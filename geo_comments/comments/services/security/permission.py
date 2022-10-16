# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment permission policy."""

from invenio_rdm_records.services.permissions import RDMRecordPermissionPolicy
from invenio_records_permissions.generators import (
    AuthenticatedUser,
    SystemProcess,
    AnyUser,
)
from invenio_records_permissions.policies.records import RecordPermissionPolicy

from .generators import CommentOwner, GeoSecretariat, IfDenied, RecordOwners


class CommentPermissionPolicy(RecordPermissionPolicy):
    """Feedback permission policy."""

    #
    # High-level permissions
    #

    # Comment related
    can_manage = [
        RecordOwners(),
        GeoSecretariat(),
        SystemProcess(),
        # CommunityAction("curate"),
    ]

    can_curate = can_manage + [CommentOwner()]

    can_view_comments = [AnyUser(), SystemProcess()]

    can_authenticated = [AuthenticatedUser(), SystemProcess()]

    #
    # Comments
    #

    # Allow record search
    can_search = [IfDenied(then_=can_curate, else_=can_view_comments)]

    # Allow reading record metadata
    can_read = [IfDenied(then_=can_curate, else_=can_view_comments)]

    # Allow submitting new record
    can_create = can_authenticated

    # Allow editing published comments
    can_update = can_curate

    # Allow deleting published comments
    can_delete = can_curate

    #
    # Comments - Management
    #

    # Allowing changing the comment state
    can_change_state = can_manage

    #
    # Comments - Related records
    #

    can_view_associated_record = RDMRecordPermissionPolicy.can_read
