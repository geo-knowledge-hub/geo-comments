# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_accounts.models import User as InvenioUser
from invenio_db import db
from invenio_records.systemfields import (
    ConstantField,
    DictField,
    ModelField,
    SystemFieldsMixin,
)
from invenio_records.models import RecordMetadataBase
from invenio_records_resources.records.systemfields import IndexField

from sqlalchemy_utils.types import UUIDType

from geo_comments.comments.records.systemfields.fields.entity import EntityField
from geo_comments.comments.records.systemfields.models import UserEntity

from .base import CommentRecordBase


#
# Generic comment type factory.
#
class CommentTypeFactory:
    """Base Factory class for comment types.

    Note:
        This class was created based on ``RecordTypeFactory`` from
        ``Invenio Records Resources``.
    """

    model_cls = None
    comment_cls = None

    _schema_path_template = (
        "https://localhost/schemas/{name_plural}/{name}-v{version}.json"
    )
    _index_name_template = "{name_plural}-{name}-v{version}"

    def __init__(
        self,
        comment_type_name,
        comment_record_entity_cls,
        comment_associated_record_cls,
        schema_path=None,
        schema_version="1.0.0",
        comment_model_cls_attr=None,
        comment_record_cls_attr=None,
        index_name=None,
    ):
        """Initializer."""
        # comment definitions
        self.comment_type_name = comment_type_name
        self.comment_name_lower = comment_type_name.lower()
        self.name_plural = f"{self.comment_name_lower}s"

        # comment classes
        self.comment_cls_attr = comment_model_cls_attr or {}
        self.comment_record_cls_attr = comment_record_cls_attr or {}
        self.comment_record_entity_cls = comment_record_entity_cls
        self.comment_associated_record_cls = comment_associated_record_cls

        # record class attributes
        self.schema_version = schema_version
        self.index_name = self._build_index_name(index_name)
        self.schema_path = self._build_schema_path(schema_path)

        # operating!
        self.create_comment_type()

    def _build_schema_path(self, optional_schema_path):
        """Build path for jsonschema."""
        if optional_schema_path:
            return optional_schema_path
        return self._schema_path_template.format(
            name_plural=self.name_plural,
            name=self.comment_name_lower,
            version=self.schema_version,
        )

    def _build_index_name(self, index_name):
        """Build index name."""
        if index_name:
            return index_name
        return self._index_name_template.format(
            name_plural=self.name_plural,
            name=self.comment_name_lower,
            version=self.schema_version,
        )

    def create_comment_type(self):
        """Create the record type."""
        self.create_metadata_model()
        self.create_record_class()

    def create_metadata_model(self):
        """Create metadata model."""
        model_class_attributes = dict(
            __tablename__=f"{self.comment_name_lower}_metadata",
            __table_args__=(db.UniqueConstraint("user_id", "record_id"),),
            **self.comment_cls_attr,
        )

        #
        # Users
        #
        model_class_attributes["user"] = db.relationship(InvenioUser)
        model_class_attributes["user_id"] = db.Column(
            db.Integer, db.ForeignKey(InvenioUser.id)
        )

        #
        # Record
        #
        model_class_attributes["record"] = db.relationship(
            self.comment_associated_record_cls
        )
        model_class_attributes["record_id"] = db.Column(
            UUIDType, db.ForeignKey(self.comment_associated_record_cls.id)
        )

        self.model_cls = type(
            f"{self.comment_type_name}Metadata",
            (db.Model, RecordMetadataBase),
            model_class_attributes,
        )

    def create_record_class(self):
        """Create record class."""
        record_class_attributes = dict(
            model_cls=self.model_cls, **self.comment_record_cls_attr
        )

        # Schema
        record_class_attributes["schema"] = ConstantField("$schema", self.schema_path)

        # Comment
        record_class_attributes["id"] = ModelField("id")
        record_class_attributes["status"] = ModelField("status")
        record_class_attributes["content"] = DictField("content")

        # Index
        record_class_attributes["index"] = IndexField(self.index_name)

        # User
        record_class_attributes["user"] = EntityField(
            key="user_id", entity_obj_class=UserEntity
        )

        # Record
        record_class_attributes["record"] = EntityField(
            key="record_id", entity_obj_class=self.comment_record_entity_cls
        )

        self.comment_cls = type(
            self.comment_type_name,
            (CommentRecordBase, SystemFieldsMixin),
            record_class_attributes,
        )


#
# Specialized comment factories
#
class FeedbackTypeFactory(CommentTypeFactory):
    """Factory class for comments."""

    def __init__(
        self,
        comment_type_name,
        comment_record_entity_cls,
        comment_associated_record_cls,
        schema_path=None,
        schema_version="1.0.0",
        comment_model_cls_attr=None,
        index_name=None,
    ):
        comment_record_cls_attr = dict(
            topics=DictField("topics")
        )  # topics must be created using topics

        super().__init__(
            comment_type_name,
            comment_record_entity_cls,
            comment_associated_record_cls,
            schema_path,
            schema_version,
            comment_model_cls_attr,
            comment_record_cls_attr,
            index_name,
        )
