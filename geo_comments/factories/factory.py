# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment type factories."""

from invenio_accounts.models import User as InvenioUser
from invenio_db import db
from invenio_records.models import RecordMetadataBase
from invenio_records.systemfields import (
    ConstantField,
    DictField,
    ModelField,
    SystemFieldsMixin,
)
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.services import pagination_links
from sqlalchemy_utils.types import UUIDType

from geo_comments.comments.records.api import CommentRecordBase, CommentStatus
from geo_comments.comments.records.systemfields.fields.entity import EntityField
from geo_comments.comments.records.systemfields.models import UserEntity
from geo_comments.comments.resources.config import CommentResourceConfig
from geo_comments.comments.resources.resource import CommentResource
from geo_comments.comments.schema import CommentSchema, FeedbackCommentSchema
from geo_comments.comments.services.config import CommentServiceConfig
from geo_comments.comments.services.links import CommentLink
from geo_comments.comments.services.security.permission import CommentPermissionPolicy
from geo_comments.comments.services.services import CommentService


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
        comment_associated_metadata_cls,
        schema_path="local://comments/comment-v1.0.0.json",
        schema_version="1.0.0",
        comment_model_cls_attr=None,
        comment_record_cls_attr=None,
        comment_service_name=None,
        comment_service_permission_policy=None,
        comment_service_endpoint_route=None,
        comment_service_endpoint_route_prefix=None,
        comment_service_search_options=None,
        comment_service_schema=CommentSchema,
        comment_service_components=None,
        comment_service_id=None,
        index_name="comments-comment-v1.0.0",
    ):
        """Initializer."""
        # comment definitions
        self.comment_type_name = comment_type_name
        self.comment_name_lower = comment_type_name.lower()
        self.name_plural = f"{self.comment_name_lower}s"

        # comment classes
        self.comment_model_cls_attr = comment_model_cls_attr or {}
        self.comment_record_cls_attr = comment_record_cls_attr or {}
        self.comment_record_entity_cls = comment_record_entity_cls

        self.comment_associated_record_cls = comment_associated_record_cls
        self.comment_associated_metadata_cls = comment_associated_metadata_cls

        # record class attributes
        self.schema_version = schema_version
        self.index_name = self._build_index_name(index_name)
        self.schema_path = self._build_schema_path(schema_path)

        # service and resources classes
        self.comment_service_cls = None
        self.comment_service_cls_config = None

        self.comment_service_endpoint_route = comment_service_endpoint_route
        self.comment_service_endpoint_route_prefix = (
            comment_service_endpoint_route_prefix
        )

        self.comment_service_id = comment_service_id
        self.comment_service_name = comment_service_name
        self.comment_service_permission_policy = comment_service_permission_policy
        self.comment_service_schema = comment_service_schema
        self.comment_service_components = comment_service_components

        self.comment_service_search_options = (
            comment_service_search_options or CommentServiceConfig.search
        )

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
        self.create_resource_class()
        self.create_service_class()

    def create_metadata_model(self):
        """Create metadata model."""
        model_class_attributes = dict(
            __tablename__=f"{self.comment_name_lower}_metadata",
            **self.comment_model_cls_attr,
        )

        # Users
        model_class_attributes["user"] = db.relationship(InvenioUser)
        model_class_attributes["user_id"] = db.Column(
            db.Integer, db.ForeignKey(InvenioUser.id)
        )

        # Record
        model_class_attributes["record"] = db.relationship(
            self.comment_associated_metadata_cls
        )
        model_class_attributes["record_id"] = db.Column(
            UUIDType, db.ForeignKey(self.comment_associated_metadata_cls.id)
        )

        # Comment
        model_class_attributes["status"] = db.Column(
            db.String, default=CommentStatus.DENIED.value
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

    def create_resource_class(self):
        """Create resource class."""
        resource_config_cls_name = f"{self.comment_type_name}ResourceConfig"
        resource_cls_name = f"{self.comment_type_name}Resource"

        route = self.comment_service_endpoint_route or f"/{self.comment_name_lower}s"

        config_cls_attributes = dict(
            blueprint_name=self.comment_name_lower,
            url_prefix=self.comment_service_endpoint_route_prefix
            or f"/{self.comment_name_lower}s",
            routes={
                # General routes
                "list": "/<pid_value>/" + route,
                "item": "/<pid_value>/" + route + "/<comment_id>",
                # Admin routes
                "deny-item": "/<pid_value>/" + route + "/<comment_id>/actions/deny",
                "allow-item": "/<pid_value>/" + route + "/<comment_id>/actions/allow",
            },
            **self.comment_model_cls_attr,
        )

        self.resource_config_cls = type(
            resource_config_cls_name,
            (CommentResourceConfig,),
            config_cls_attributes,
        )

        self.resource_cls = type(resource_cls_name, (CommentResource,), {})

    def create_service_class(self):
        """Create a service class."""
        config_cls_name = f"{self.comment_service_name}ServiceConfig"
        service_cls_name = f"{self.comment_service_name}Service"
        permission_policy_cls_name = f"{self.comment_service_name}PermissionPolicy"

        if not self.comment_service_permission_policy:
            self.comment_service_permission_policy = type(
                permission_policy_cls_name, (CommentPermissionPolicy,), {}
            )

        route = self.comment_service_endpoint_route or f"/{self.comment_name_lower}s"

        config_cls_attributes = dict(
            permission_policy_cls=self.comment_service_permission_policy,
            record_cls=self.comment_cls,
            record_associated_cls=self.comment_associated_record_cls,
            search=self.comment_service_search_options,
            schema=self.comment_service_schema,
            links_item={"self": CommentLink("{+api}/" + route + "?q=id:{id}")},
            links_search=pagination_links("{+api}/" + route + "{?args*}"),
            links_action={
                "allow": CommentLink(
                    "{+api}/" + route + "/actions/allow?q=id:{id}",
                ),
                "deny": CommentLink(
                    "{+api}/" + route + "/actions/deny?q=id:{id}",
                ),
            },
        )

        if self.comment_service_components:
            config_cls_attributes.update(
                dict(components=self.comment_service_components)
            )

        if self.comment_service_id:
            config_cls_attributes.update(
                dict(
                    service_id=self.comment_service_id,
                    indexer_queue_name=self.comment_service_id,
                )
            )

        self.comment_service_cls_config = type(
            config_cls_name, (CommentServiceConfig,), config_cls_attributes
        )

        self.comment_service_cls = type(service_cls_name, (CommentService,), {})


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
        comment_associated_metadata_cls,
        **kwargs,
    ):
        """Initializer."""
        # Defining the properties to create a feedback specialized comment type

        # Index name
        index_name = "feedbacks-feedback-v1.0.0"

        # Schema path
        schema_path = "local://feedbacks/feedback-v1.0.0.json"

        # Topics support (Only for feedbacks)
        comment_record_cls_attr = dict(topics=DictField("topics"))

        # Users can send only one feedback
        comment_model_cls_attr = dict(
            __table_args__=(db.UniqueConstraint("user_id", "record_id"),),
        )

        super().__init__(
            comment_type_name,
            comment_record_entity_cls,
            comment_associated_record_cls,
            comment_associated_metadata_cls,
            index_name=index_name,
            schema_path=schema_path,
            comment_record_cls_attr=comment_record_cls_attr,
            comment_model_cls_attr=comment_model_cls_attr,
            comment_service_schema=FeedbackCommentSchema,
            **kwargs,
        )
