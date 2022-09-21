# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service schema."""

from marshmallow import fields

from geo_comments.comments.schema import FeedbackCommentSchema as BaseCommentSchema
from geo_comments.comments.schema import generate_permission_schema_document
from geo_comments.proxies import current_comments


class FeedbackCommentSchema(BaseCommentSchema):
    """Comment schema class."""

    permissions = fields.Method("get_permissions", dump_only=True)

    def get_permissions(self, obj):
        """Return permissions to act on comments or empty dict."""
        service = current_comments.resource_feedback_service
        return generate_permission_schema_document(
            self.context["identity"], service, obj
        )
