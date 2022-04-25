# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import marshmallow as ma

from flask_resources import (
    ResourceConfig,
    ResponseHandler,
    JSONSerializer,
    RequestBodyParser,
    JSONDeserializer,
)


from invenio_records_resources.resources.records.headers import etag_headers
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema


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
