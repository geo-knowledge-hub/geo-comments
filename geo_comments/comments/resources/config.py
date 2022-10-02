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


class CommentResourceConfig(ResourceConfig):
    """Comment resource configuration class."""

    # Blueprint configuration
    url_prefix = None
    blueprint_name = None

    # Request parsing
    request_read_args = {}
    request_search_args = SearchRequestArgsSchema
    request_headers = {"if_match": ma.fields.Int()}
    request_comment_view_args = {
        "comment_id": ma.fields.UUID(),
        "pid_value": ma.fields.Str(),
    }

    request_extra_args = {"expand": ma.fields.Boolean()}

    request_body_parsers = {"application/json": RequestBodyParser(JSONDeserializer())}

    response_handlers = {
        "application/json": ResponseHandler(JSONSerializer(), headers=etag_headers)
    }

    default_content_type = "application/json"
    default_accept_mimetype = "application/json"
