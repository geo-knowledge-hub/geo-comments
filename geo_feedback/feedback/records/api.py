# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from invenio_db import db

from invenio_records.systemfields import (
    SystemFieldsMixin,
    DictField,
    ModelField,
    ConstantField,
)

from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField

from geo_feedback.feedback.records.models import FeedbackModel
from geo_feedback.feedback.records.systemfields.fields.entity import EntityField
from geo_feedback.feedback.records.systemfields.models import RecordEntity, UserEntity


class FeedbackRecordBase(Record):
    """Base for Feedback record High-level API."""

    @classmethod
    def get_record(cls, id_, with_deleted=False, with_denied=False):
        """Retrieve the record by id."""
        with db.session.no_autoflush:
            query = cls.model_cls.query.filter_by(id=id_)

            if not with_deleted:
                query = query.filter(cls.model_cls.is_deleted != True)  # noqa

            if not with_denied:
                query = query.filter(cls.model_cls.status != "D")  # noqa

            obj = query.one()
            return cls(obj.data, model=obj)

    @classmethod
    def get_records(cls, ids, with_deleted=False, with_denied=False):
        """Retrieve multiple records by id."""
        with db.session.no_autoflush:
            query = cls.model_cls.query.filter(cls.model_cls.id.in_(ids))

            if not with_deleted:
                query = query.filter(cls.model_cls.is_deleted != True)  # noqa

            if not with_denied:
                query = query.filter(cls.model_cls.status != "D")  # noqa

            return [cls(obj.data, model=obj) for obj in query.all()]


class FeedbackRecord(FeedbackRecordBase, SystemFieldsMixin):
    """Feedback High-level API."""

    #
    # System fields
    #
    schema = ConstantField("$schema", "local://feedback/feedback-v1.0.0.json")

    # Feedback
    id = ModelField("id")

    status = ModelField("status")

    topics = DictField("topics")
    comment = DictField("comment")

    # Relations
    user = EntityField(key="user_id", entity_obj_class=UserEntity)
    record = EntityField(key="record_id", entity_obj_class=RecordEntity)

    # Database model and Index
    model_cls = FeedbackModel
    index = IndexField("feedback-feedback-v1.0.0", search_alias="feedback")
