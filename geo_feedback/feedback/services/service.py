# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from invenio_db import db
from invenio_records_resources.services.base import Service as InvenioBaseService


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

    def _resolve_record(self, pid_value):
        return self.record_cls.pid.resolve(pid_value, registered_only=True)

    def list_record_feedback(self, identity, is_deleted=None, is_approved=None, **kwargs):
        self.require_permission(identity, "read")

        record_id = (
            self._resolve_record(kwargs.get("pid_value")).id if "pid_value" in kwargs else None
        )

        kwargs = {
            "is_deleted": is_deleted,
            "is_approved": is_approved,

            "record_id": record_id,

            **kwargs
        }

        return self.feedback_cls.get_records(**kwargs)

    def search_record_feedback(self, identity, **kwargs):
        self.require_permission(identity, "curate")

        return self.list_record_feedback(identity, **kwargs)

    def get_feedback(self, identity, pid_value, feedback_id):
        self.require_permission(identity, "read")

        record = self._resolve_record(pid_value)
        feedback = self.feedback_cls.get_record(id_=feedback_id, record_id=record.id)

        return feedback

    def create_feedback(self, identity, pid_value, data, **kwargs):
        self.require_permission(identity, "create")

        # checking schema
        self.schema.load(data)

        # creating an empty feedback
        feedback = self.feedback_cls.create({})

        # searching for feedback record
        record = self._resolve_record(pid_value)

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

        feedback.commit()
        db.session.commit()

        return feedback

    def edit_feedback(self, identity, pid_value, feedback_id, data):
        self.require_permission(identity, "edit")

        # checking schema
        self.schema.load(data)

        record = self._resolve_record(pid_value)
        feedback = self.feedback_cls.get_record(id_=feedback_id, record_id=record.id)

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

    def delete_feedback(self, identity, pid_value, feedback_id):
        self.require_permission(identity, "delete")

        # searching for feedback record
        record = self._resolve_record(pid_value)

        feedback = self.feedback_cls.get_record(id_=feedback_id, record_id=record.id, with_denied=True)

        # running the components
        for component in self.components:
            if hasattr(component, "delete_feedback"):
                component.delete_feedback(
                    identity,
                    record=record,
                    feedback=feedback
                )

        feedback.delete()
        db.session.commit()

        return feedback

    def _change_feedback_state(self, identity, pid_value, feedback_id, state):
        self.require_permission(identity, "change_state")

        # searching
        record = self._resolve_record(pid_value)
        feedback = self.feedback_cls.get_record(id_=feedback_id, record_id=record.id, with_denied=True)

        # running the components
        for component in self.components:
            if hasattr(component, "change_feedback_state"):
                component.change_feedback_state(
                    identity,
                    data=state,
                    record=record,
                    feedback=feedback
                )

        # changing state
        feedback.is_approved = state

        feedback.commit()
        db.session.commit()

        return feedback

    def approve_feedback(self, identity, pid_value, feedback_id):
        return self._change_feedback_state(identity, pid_value, feedback_id, True)

    def deny_feedback(self, identity, pid_value, feedback_id):
        return self._change_feedback_state(identity, pid_value, feedback_id, False)


__all__ = (
    "UserFeedbackService"
)
