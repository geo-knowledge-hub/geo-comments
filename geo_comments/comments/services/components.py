# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Feedback service components."""

from invenio_records_resources.services.records.components import (
    ServiceComponent as BaseServiceComponent,
)

from geo_comments.comments.records.api import CommentStatus


class FeedbackComponentBase(BaseServiceComponent):
    """Base Feedback component."""

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

    def delete(self, identity, feedback=None, **kwargs):
        """Delete handler."""
        pass

    def update(self, identity, feedback=None, data=None):
        """Update handler."""
        pass

    def change_feedback_state(self, identity, feedback=None, state=None, **kwargs):
        """State handler."""
        pass


class FeedbackData(FeedbackComponentBase):
    """Component to fill feedback records."""

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
        # adding data
        feedback.update(data)

        # user and record
        feedback.record = record.id
        feedback.user = identity.user.id

        # checking auto approve
        if auto_approve:
            feedback.status = CommentStatus.ALLOWED.value

    def update(self, identity, feedback=None, data=None):
        """Update handler."""
        feedback.update(data)

    def change_feedback_state(
        self,
        identity,
        feedback=None,
        state=None,
        data=None,
        auto_approve=False,
        **kwargs
    ):
        """State handler."""
        feedback.status = data.value
