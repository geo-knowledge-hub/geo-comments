# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Data model for GEO Knowledge Hub User's Feedback Component."""

import uuid

from enum import Enum

from invenio_db import db
from invenio_records.models import RecordMetadataBase

from sqlalchemy_utils.types import UUIDType

from invenio_accounts.models import User as InvenioUser
from invenio_rdm_records.records.models import RDMRecordMetadata as InvenioRecordMetadata


class FeedbackStatus(Enum):
    ALLOWED = "A"
    DENIED = "D"


class UserFeedbackMetadata(db.Model, RecordMetadataBase):
    """Represent a user feedback record."""
    __tablename__ = "feedbacks_user_feedback"

    id = db.Column(
        UUIDType,
        primary_key=True,
        default=uuid.uuid4,
    )

    status = db.Column(db.String, default=FeedbackStatus.DENIED.value)  # A(llowed) or D(enied)

    user_id = db.Column(db.Integer, db.ForeignKey(InvenioUser.id))
    user = db.relationship(InvenioUser)

    record_metadata_id = db.Column(UUIDType, db.ForeignKey(InvenioRecordMetadata.id))
    record_metadata = db.relationship(InvenioRecordMetadata)

    version_id = None
    __mapper_args__ = {}

    __table_args__ = (db.UniqueConstraint("user_id", "record_metadata_id"),)


__all__ = (
    "FeedbackStatus",

    "UserFeedbackMetadata"
)
