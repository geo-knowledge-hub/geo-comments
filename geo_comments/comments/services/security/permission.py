# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment permission policy."""

from geo_config.security.generators import GeoSecretariat
from invenio_rdm_records.services.generators import (
    CommunityAction,
    RecordOwners,
    SecretLinks,
)
from invenio_records_permissions.generators import AuthenticatedUser, SystemProcess
from invenio_records_permissions.policies.records import RecordPermissionPolicy

from geo_comments.comments.services.security.generators import CommentOwner, IfDenied


class FeedbackPermissionPolicy(RecordPermissionPolicy):
    """Feedback permission policy."""

    #
    # High-level permissions
    #

    # Record related
    can_view_associated_record = [
        RecordOwners(),
        SecretLinks("view"),
        CommunityAction("view"),
    ]

    # Comment related
    can_manage = [
        RecordOwners(),
        GeoSecretariat(),
        CommunityAction("curate"),
        SystemProcess(),
    ]

    can_curate = can_manage + [CommentOwner()]

    can_view_comments = [AuthenticatedUser(), SystemProcess()]

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

    # Allow editing published ratings
    can_update = can_curate

    # Allow deleting
    can_delete = can_curate
