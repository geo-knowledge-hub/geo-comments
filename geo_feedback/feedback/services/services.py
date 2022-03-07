# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from invenio_records_resources.services.records import (
    RecordService as InvenioBaseService,
)

from invenio_records_resources.services.uow import (
    RecordCommitOp,
    RecordDeleteOp,
    unit_of_work,
)

from invenio_rdm_records.services.services import RDMRecordService

from geo_feedback.feedback.records.models import FeedbackStatus
from geo_feedback.feedback.services.links import ActionLinksTemplate


class FeedbackRecordService(RDMRecordService):
    """Feedback record service class."""


class FeedbackService(InvenioBaseService):
    """Feedback service class."""

    def __init__(self, config, record_service=None):
        super(FeedbackService, self).__init__(config)

        self._record_service = record_service

    @property
    def links_item_tpl(self):
        """Item links template."""
        return ActionLinksTemplate(self.config.links_item, self.config.links_action)

    @unit_of_work()
    def _create(
        self,
        record_cls,
        identity,
        recid,
        data,
        auto_approve=False,
        raise_errors=True,
        uow=None,
    ):
        """Create a feedback record."""
        self.require_permission(identity, "create")

        # checking schema
        data, errors = self.schema.load(
            data, context={"identity": identity}, raise_errors=raise_errors
        )

        # creating an empty feedback
        feedback = record_cls.create({})

        # searching for feedback record
        record = self._record_service.read(id_=recid, identity=identity)

        # running the components
        self.run_components(
            "create",
            identity,
            data=data,
            record=record._obj,
            feedback=feedback,
            auto_approve=auto_approve,
            errors=errors,
            uow=uow,
        )

        # Persist record (DB and index)
        uow.register(RecordCommitOp(feedback, self.indexer))

        return self.result_item(
            self, identity, feedback, links_tpl=self.links_item_tpl, errors=errors
        )

    @unit_of_work()
    def create(self, identity, recid, data, auto_approve=False, uow=None):
        """Create a feedback record."""
        return self._create(
            self.record_cls, identity, recid, data, auto_approve=auto_approve, uow=uow
        )

    def read(self, identity, feedback_id):
        """Read a feedback matching the id."""
        # reading the feedback
        feedback = self.record_cls.get_record(id_=feedback_id)

        self.require_permission(identity, "read", record=feedback)

        return self.result_item(
            self,
            identity,
            feedback,
            links_tpl=self.links_item_tpl,
        )

    @unit_of_work()
    def update(self, feedback_id, identity, data, uow=None):
        """Replace a record."""
        feedback = self.record_cls.get_record(id_=feedback_id)

        # Permissions
        self.require_permission(identity, "update", record=feedback)

        data, _ = self.schema.load(
            data,
            context={"identity": identity},
        )

        # Run components
        self.run_components(
            "update",
            identity,
            data=data,
            feedback=feedback,
            uow=uow,
        )

        uow.register(RecordCommitOp(feedback, self.indexer))

        return self.result_item(
            self,
            identity,
            feedback,
            links_tpl=self.links_item_tpl,
        )

    @unit_of_work()
    def delete(self, feedback_id, identity, uow=None):
        """Delete a feedback from database and search indexes."""
        feedback = self.record_cls.get_record(id_=feedback_id)

        # Permissions
        self.require_permission(identity, "delete", record=feedback)

        # Run components
        self.run_components(
            "delete",
            identity,
            feedback=feedback,
            uow=uow,
        )

        uow.register(
            RecordDeleteOp(feedback, self.indexer, index_refresh=True, force=True)
        )

        return True

    @unit_of_work()
    def _change_feedback_status(self, identity, feedback_id, status, uow=None):
        self.require_permission(identity, "change_state")

        # searching
        feedback = self.record_cls.get_record(id_=feedback_id, with_denied=True)

        # running the components
        self.run_components(
            "change_feedback_state",
            identity,
            data=status,
            feedback=feedback,
            uow=uow,
        )

        uow.register(RecordCommitOp(feedback, self.indexer))

        return self.result_item(self, identity, feedback, links_tpl=self.links_item_tpl)

    @unit_of_work()
    def allow_feedback(self, identity, feedback_id, uow=None):
        return self._change_feedback_status(
            identity, feedback_id, FeedbackStatus.ALLOWED, uow=uow
        )

    @unit_of_work()
    def deny_feedback(self, identity, feedback_id, uow=None):
        return self._change_feedback_status(
            identity, feedback_id, FeedbackStatus.DENIED, uow=uow
        )
