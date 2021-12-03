# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from invenio_db import db
from invenio_records.systemfields import SystemFieldsMixin, DictField, ModelField

from .models import UserFeedbackMetadata

from invenio_records_resources.records.api import Record


class FeedbackRecordBase(Record, SystemFieldsMixin):

    def revert(self, revision_id):
        """Revert the record to a specific revision."""
        raise NotImplementedError("`revert` is not available for FeedbackRecord classes.")

    @property
    def revisions(self):
        """Get revisions iterator."""
        raise NotImplementedError("`revisions` is not available for FeedbackRecord classes.")

    @property
    def revision_id(self):
        """Get revision identifier."""
        raise NotImplementedError("`revision_id` is not available for FeedbackRecord classes.")

    @classmethod
    def get_record(cls, id=None, with_denied=False):
        """Retrieve the record by id.

        Raise a database exception if the record does not exist.

        Args:
            id (str): Feedback record id

            with_denied (bool): If `True` then it includes denied feedback records.

        Returns:
            Record: The :class:`Record` instance.
        """
        with db.session.no_autoflush:
            # Searching by the id
            query = cls.model_cls.query.filter_by(id=id)

            if not with_denied:
                query = query.filter(cls.model_cls.status != "D")  # noqa

            obj = query.one()
            return cls(obj.data, model=obj)

    @classmethod
    def get_records(cls, recid=None, **kwargs):
        """Retrieve the record by id.

        Raise a database exception if the record does not exist.

        Args:
            recid (str): Record (id) associated with the feedbacks.

            kwargs (dict): Query params.
        Returns:
            List: List of retrieved records.
        """
        # filtering invalid parameters
        valid_query_parameters = ["id", "status", "user_id"]
        query_arguments = {k: v for k, v in kwargs.items() if v is not None and k in valid_query_parameters}

        with db.session.no_autoflush:
            # Searching by the id
            query = cls.model_cls.query.filter_by(**query_arguments)

            # Filtering record
            if recid:
                query = query.filter(cls.model_cls.record_metadata_id == recid)  # noqa

            objs = query.all()
            return [cls(obj.data, model=obj) for obj in objs]


class FeedbackRecord(FeedbackRecordBase):
    model_cls = UserFeedbackMetadata

    #
    # Relation fields
    #
    user = ModelField()
    user_id = ModelField()

    record_metadata = ModelField()
    record_metadata_id = ModelField()

    #
    # Comment fields
    #
    status = ModelField()

    topics = DictField("topics")
    comment = DictField("comment")

    #
    # Schema (ToDo)
    #
    # schema = ConstantField("$schema", "local://...")

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "author": self.user.profile.full_name,
            "topics": self.topics,
            "comment": self.comment,
            "created": self.created,
            "updated": self.updated
        }


__all__ = (
    "FeedbackRecord"
)
