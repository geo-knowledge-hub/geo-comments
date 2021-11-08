# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_db import db
from invenio_records.api import Record
from invenio_records.systemfields import SystemFieldsMixin, DictField, ModelField

from .models import UserFeedbackMetadata


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
    def get_record(cls, id_, record_id, with_deleted=False, with_denied=False):
        """Retrieve the record by id.

        Raise a database exception if the record does not exist.

        :param id_: feedback ID.
        :param record_id: record ID.
        :param with_deleted: If `True` then it includes deleted feedback records.
        :param with_denied: If `True` then it includes denied feedback records.
        :returns: The :class:`Record` instance.
        """
        with db.session.no_autoflush:
            # Searching by the id
            query = cls.model_cls.query.filter_by(id=id_)

            # Filtering record
            query = query.filter(cls.model_cls.record_metadata_id == record_id)  # noqa

            if not with_deleted:
                query = query.filter(cls.model_cls.is_deleted != True)  # noqa

            if not with_denied:
                query = query.filter(cls.model_cls.is_approved != False)  # noqa

            obj = query.one()
            return cls(obj.data, model=obj)

    @classmethod
    def get_records(cls, record_id=None, **kwargs):
        """Retrieve the record by id.

        Raise a database exception if the record does not exist.

        :param record_id:
        :param kwargs: Query parameters.

        :returns: The :class:`Record` instance.
        """
        # filtering invalid parameters
        valid_query_parameters = ["id", "is_approved", "is_deleted", "user_id", "record_id"]
        query_arguments = {k: v for k, v in kwargs.items() if v is not None and k in valid_query_parameters}

        with db.session.no_autoflush:
            # Searching by the id
            query = cls.model_cls.query.filter_by(**query_arguments)

            # Filtering record
            if record_id:
                query = query.filter(cls.model_cls.record_metadata_id == record_id)  # noqa

            objs = query.all()
            return [cls(obj.data, model=obj) for obj in objs]


class FeedbackRecord(FeedbackRecordBase):
    model_cls = UserFeedbackMetadata

    #
    # Model fields
    #
    json = DictField(clear_none=True, create_if_missing=True)

    is_approved = ModelField(dump=False)

    user = ModelField()
    user_id = ModelField()

    record_metadata = ModelField()
    record_metadata_id = ModelField()

    #
    # Comment fields
    #
    text = DictField("comment")
    categories = DictField("categories")

    #
    # Schema (ToDo)
    #
    # schema = ConstantField("$schema", "local://...")

    def to_dict(self):
        return {
            "id": self.id,
            "author": {
                "fullname": self.user.profile.full_name,
                "email": self.user.email
            },
            "is_approved": self.is_approved,
            "is_deleted": self.is_deleted,
            **(self.json or {})
        }

    __all__ = (
        "FeedbackRecord"
    )
