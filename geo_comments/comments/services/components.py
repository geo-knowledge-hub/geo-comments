# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment service components."""

from invenio_records_resources.services.records.components import (
    ServiceComponent as BaseServiceComponent,
)

from geo_comments.comments.records.api import CommentStatus


class CommentComponentBase(BaseServiceComponent):
    """Base Comment component."""

    def create(
        self,
        identity,
        feedback=None,
        data=None,
        record=None,
        auto_approve=False,
        **kwargs
    ):
        """Create handler."""
        pass

    def delete(self, identity, comment=None, **kwargs):
        """Delete handler."""
        pass

    def update(self, identity, comment=None, data=None):
        """Update handler."""
        pass

    def change_comment_state(self, identity, comment=None, state=None, **kwargs):
        """State handler."""
        pass


class CommentData(CommentComponentBase):
    """Component to fill comment records."""

    def create(
        self,
        identity,
        comment=None,
        data=None,
        associated_record=None,
        auto_approve=False,
        **kwargs
    ):
        """Create handler."""
        # adding data
        comment.update(data)

        # user and record
        comment.record = associated_record.id
        comment.user = identity.id

        # checking auto approve
        if auto_approve:
            comment.status = CommentStatus.ALLOWED.value

    def update(self, identity, comment=None, data=None):
        """Update handler."""
        comment.update(data)

    def change_comment_state(
        self,
        identity,
        comment=None,
        state=None,
        data=None,
        auto_approve=False,
        **kwargs
    ):
        """State handler."""
        comment.status = data.value
