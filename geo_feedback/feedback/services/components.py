# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.services.records.components import \
    ServiceComponent as BaseServiceComponent

from ..records.models import FeedbackStatus


class UserFeedbackComponentBase(BaseServiceComponent):

    def change_feedback_state(self, identity, feedback=None, state=None, **kwargs):
        pass

    def create_feedback(self, identity, feedback=None, data=None, record=None, **kwargs):
        pass

    def delete_feedback(self, identity, feedback=None, **kwargs):
        pass

    def edit_feedback(self, identity, feedback=None, data=None):
        pass


class UserFeedbackMetadata(UserFeedbackComponentBase):

    def create_feedback(self, identity, feedback=None, data=None, record=None, **kwargs):
        # Adding data
        feedback.update(data)

        feedback.user_id = identity.user.id
        feedback.record_metadata_id = record.id

        # checking auto approve
        auto_approve = kwargs.get("auto_approve", False)
        if auto_approve:
            feedback.status = FeedbackStatus.ALLOWED.value

    def edit_feedback(self, identity, feedback=None, data=None):
        feedback.update(data)

    def change_feedback_state(self, identity, feedback=None, state=None, data=None, **kwargs):
        feedback.status = data.value


__all__ = (
    "UserFeedbackMetadata"
)
