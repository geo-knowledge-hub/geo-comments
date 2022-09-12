# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment resource config."""

import marshmallow as ma
from flask_resources import (
    JSONDeserializer,
    JSONSerializer,
    RequestBodyParser,
    ResourceConfig,
    ResponseHandler,
)
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema
from invenio_records_resources.resources.records.headers import etag_headers


class BaseResourceConfig(ResourceConfig):
    """Base resource configuration class."""

    # Blueprint configuration
    url_prefix = None

    # Request parsing
    request_read_args = {}
    request_search_args = SearchRequestArgsSchema
    request_headers = {"if_match": ma.fields.Int()}
    request_comment_view_args = {
        "comment_id": ma.fields.UUID(required=True),
        "pid_value": ma.fields.Str(),
    }

    request_body_parsers = {"application/json": RequestBodyParser(JSONDeserializer())}

    response_handlers = {
        "application/json": ResponseHandler(JSONSerializer(), headers=etag_headers)
    }

    default_content_type = "application/json"
    default_accept_mimetype = "application/json"


class CommentResourceConfig(BaseResourceConfig):
    """Comments resource."""

    # Blueprint configuration
    blueprint_name = "geo_comments_comments"

    routes = {
        # General routes
        "list": "/<pid_value>/comments",
        "item": "/<pid_value>/comments/<comment_id>",
        # Admin routes
        "deny-item": "/<pid_value>/comments/<comment_id>/actions/deny",
        "allow-item": "/<pid_value>/comments/<comment_id>/actions/allow",
    }


class FeedbackResourceConfig(BaseResourceConfig):
    """Feedback resource."""

    # Blueprint configuration
    blueprint_name = "geo_comments_feedbacks"

    routes = {
        # General routes
        "list": "/<pid_value>/feedbacks",
        "item": "/<pid_value>/feedbacks/<comment_id>",
        # Admin routes
        "deny-item": "/<pid_value>/feedbacks/<comment_id>/actions/deny",
        "allow-item": "/<pid_value>/feedbacks/<comment_id>/actions/allow",
    }
