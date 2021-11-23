# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from invenio_db import db
from invenio_records_resources.services.base import Service as InvenioBaseService

from ..records.models import FeedbackStatus


class UserFeedbackService(InvenioBaseService):

    def __init__(self, config):
        super(UserFeedbackService, self).__init__(config)

    @property
    def schema(self):
        return self.config.schema()

    @property
    def record_cls(self):
        return self.config.record_cls

    @property
    def feedback_cls(self):
        return self.config.feedback_cls

    def _resolve_record(self, recid):
        return self.record_cls.pid.resolve(recid, registered_only=True)

    def list_record_feedback(self, identity, **kwargs):
        self.require_permission(identity, "read")

        recid = (
            self._resolve_record(kwargs.get("recid")).id if "recid" in kwargs else None
        )

        kwargs.update({"recid": recid})
        return self.feedback_cls.get_records(**kwargs)

    def search_record_feedback(self, identity, **kwargs):
        self.require_permission(identity, "curate")

        return self.list_record_feedback(identity, **kwargs)

    def get_feedback(self, identity, feedback_id):
        self.require_permission(identity, "read")

        return self.feedback_cls.get_record(id=feedback_id)

    def create_feedback(self, identity, recid, data, **kwargs):
        self.require_permission(identity, "create")

        # checking schema
        self.schema.load(data)

        # creating an empty feedback
        feedback = self.feedback_cls.create({})

        # searching for feedback record
        record = self._resolve_record(recid)

        # running the components
        for component in self.components:
            if hasattr(component, "create_feedback"):
                component.create_feedback(
                    identity,
                    data=data,
                    record=record,
                    feedback=feedback,
                    **kwargs
                )

        try:
            feedback.commit()
            db.session.commit()
        finally:
            db.session.rollback()

        return feedback

    def edit_feedback(self, identity, feedback_id, data):
        self.require_permission(identity, "edit")

        # checking schema
        self.schema.load(data)

        # all type of records can be edited
        feedback = self.feedback_cls.get_record(id=feedback_id, with_denied=False)

        # running the components
        for component in self.components:
            if hasattr(component, "edit_feedback"):
                component.edit_feedback(
                    identity,
                    data=data,
                    feedback=feedback
                )

        feedback.commit()
        db.session.commit()

        return feedback

    def delete_feedback(self, identity, feedback_id):
        self.require_permission(identity, "delete")

        # searching for feedback record
        feedback = self.feedback_cls.get_record(id=feedback_id, with_denied=True)

        # running the components
        for component in self.components:
            if hasattr(component, "delete_feedback"):
                component.delete_feedback(
                    identity,
                    feedback=feedback
                )

        feedback.delete(force=True)
        db.session.commit()

        return feedback

    def _change_feedback_status(self, identity, feedback_id, status):
        self.require_permission(identity, "change_state")

        # searching
        feedback = self.feedback_cls.get_record(id=feedback_id, with_denied=True)

        # running the components
        for component in self.components:
            if hasattr(component, "change_feedback_state"):
                component.change_feedback_state(
                    identity,
                    data=status,
                    feedback=feedback
                )

        feedback.commit()
        db.session.commit()

        return feedback

    def allow_feedback(self, identity, feedback_id):
        return self._change_feedback_status(identity, feedback_id, FeedbackStatus.ALLOWED)

    def deny_feedback(self, identity, feedback_id):
        return self._change_feedback_status(identity, feedback_id, FeedbackStatus.DENIED)


__all__ = (
    "UserFeedbackService"
)
