# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_db import db
from invenio_records.models import RecordMetadataBase

from sqlalchemy_json import mutable_json_type

from sqlalchemy_utils.types import UUIDType
from sqlalchemy.dialects.postgresql import JSONB

from invenio_accounts.models import User as InvenioUser
from invenio_rdm_records.records.models import RDMRecordMetadata as InvenioRecordMetadata


class UserFeedbackMetadata(db.Model, RecordMetadataBase):
    __tablename__ = "users_feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    json = db.Column(mutable_json_type(dbtype=JSONB(none_as_null=True), nested=True), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey(InvenioUser.id))
    user = db.relationship(InvenioUser)

    record_metadata_id = db.Column(UUIDType, db.ForeignKey(InvenioRecordMetadata.id))
    record_metadata = db.relationship(InvenioRecordMetadata)

    version_id = None
    __mapper_args__ = {}


__all__ = (
    "UserFeedbackMetadata"
)
