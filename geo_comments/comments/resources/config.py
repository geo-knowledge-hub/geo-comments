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


class FeedbackResourceConfig(ResourceConfig):
    """Feedback resource configuration class."""

    # Blueprint configuration
    url_prefix = "/feedbacks"
    blueprint_name = "geo_feedback"
    routes = {
        # General routes
        "list": "",
        "item": "<fid>",
        # Admin routes
        "deny-item": "/actions/deny",
        "allow-item": "/actions/allow",
    }

    # Request parsing
    request_read_args = {}
    request_search_args = SearchRequestArgsSchema
    request_headers = {"if_match": ma.fields.Int()}
    request_feedback_view_args = {"fid": ma.fields.UUID(required=True)}

    request_body_parsers = {"application/json": RequestBodyParser(JSONDeserializer())}

    response_handlers = {
        "application/json": ResponseHandler(JSONSerializer(), headers=etag_headers)
    }

    default_content_type = "application/json"
    default_accept_mimetype = "application/json"
