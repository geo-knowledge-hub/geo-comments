# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Data model for GEO Knowledge Hub User's Feedback Component."""

from enum import Enum

from invenio_accounts.models import User as InvenioUser
from invenio_db import db
from invenio_rdm_records.records.models import (
    RDMRecordMetadata as InvenioRecordMetadata,
)
from invenio_records.models import RecordMetadataBase
from sqlalchemy_utils.types import UUIDType


class FeedbackStatus(Enum):
    """Feedback status enum.

    Allowed: The feedback is approved and can be presented for the users;
    Denied: The feedback is denied and can't be presented for the users.
    """

    ALLOWED = "A"
    DENIED = "D"


class FeedbackModel(db.Model, RecordMetadataBase):
    """Feedback model class."""

    __tablename__ = "feedbacks_feedback"

    #
    # Users
    #
    user_id = db.Column(db.Integer, db.ForeignKey(InvenioUser.id))
    user = db.relationship(InvenioUser)

    #
    # Records
    #
    record_id = db.Column(UUIDType, db.ForeignKey(InvenioRecordMetadata.id))
    record = db.relationship(InvenioRecordMetadata)

    #
    # Feedback
    #
    status = db.Column(
        db.String, default=FeedbackStatus.DENIED.value
    )  # A(llowed) or D(enied)

    __table_args__ = (db.UniqueConstraint("user_id", "record_id"),)
