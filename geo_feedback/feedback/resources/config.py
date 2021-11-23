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
    HTTPJSONException,
    create_error_handler
)

from sqlalchemy.exc import IntegrityError

feedback_error_handlers = {
    IntegrityError: create_error_handler(
        HTTPJSONException(
            code=409,
            description="User have already created feedback for this record."
        )
    )
}


class UserFeedbackResourceConfig(ResourceConfig):
    url_prefix = "/feedbacks"
    blueprint_name = "geo_feedback"

    request_view_args = {
        "feedback_id": ma.fields.UUID(),
        "recid": ma.fields.String()
    }

    request_search_args = {
        # properties
        "id": ma.fields.String(),
        "user_id": ma.fields.Int(),

        # status
        "status": ma.fields.Str(),

        "recid": ma.fields.String()
    }

    routes = {
        # General routes
        "list-item": "/records/<recid>",  # only approved feedbacks
        "create-item": "/records/<recid>",
        "get-item": "/<feedback_id>",
        "update-item": "/<feedback_id>",
        "delete-item": "/<feedback_id>",

        # Admin routes
        "search-item": "",  # feedbacks from all records (approved and denied)
        "deny-item": "/<feedback_id>/actions/deny",
        "allow-item": "/<feedback_id>/actions/allow"
    }

    # Request parsing
    request_headers = {
        "if_match": ma.fields.Int()
    }

    request_body_parsers = {
        "application/json": RequestBodyParser(JSONDeserializer())
    }

    response_handlers = {
        "application/json": ResponseHandler(
            JSONSerializer()
        )
    }

    default_content_type = "application/json"
    default_accept_mimetype = "application/json"

    error_handlers = feedback_error_handlers


__all__ = (
    "UserFeedbackResourceConfig"
)
