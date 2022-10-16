# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comments base API class."""

from enum import Enum

from invenio_db import db
from invenio_records_resources.records.api import Record


class CommentStatus(Enum):
    """Comment status enum.

    Allowed: The comment is approved and can be presented for the users;
    Denied: The comment is denied and can't be presented for the users.
    """

    ALLOWED = "A"
    DENIED = "D"


class CommentRecordBase(Record):
    """Base for Feedback record High-level API."""

    @classmethod
    def get_record_by_user_record(
        cls, record_id, user_id, with_deleted=False, with_denied=False
    ):
        """Retrieve record by record and user id."""
        with db.session.no_autoflush:
            query = cls.model_cls.query.filter_by(record=record_id, user=user_id)

            if not with_deleted:
                query = query.filter(cls.model_cls.is_deleted != True)  # noqa

            if not with_denied:
                query = query.filter(cls.model_cls.status != "D")  # noqa

            return [cls(obj.data, model=obj) for obj in query.all()]

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
