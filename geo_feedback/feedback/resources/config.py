# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


import marshmallow as ma
from flask_resources import ResourceConfig, ResponseHandler, JSONSerializer, RequestBodyParser, JSONDeserializer


class UserFeedbackResourceConfig(ResourceConfig):
    url_prefix = "/feedback"
    blueprint_name = "geo_feedback"

    request_view_args = {
        "feedback_id": ma.fields.Int(),
        "pid_value": ma.fields.String()
    }

    request_search_args = {
        # properties
        "id": ma.fields.Int(),
        "user_id": ma.fields.Int(),

        # status
        "is_approved": ma.fields.Bool(),
        "is_deleted": ma.fields.Bool(),

        "record_id": ma.fields.String()
    }

    routes = {
        # General routes
        "list-item": "/<pid_value>",  # only approved feedbacks
        "create-item": "/<pid_value>",
        "get-item": "/<pid_value>/<feedback_id>",
        "update-item": "/<pid_value>/<feedback_id>",
        "delete-item": "/<pid_value>/<feedback_id>",

        # Admin routes
        "search-item": "",  # feedbacks from all records (approved and denied)
        "deny-item": "/<pid_value>/<feedback_id>/actions/deny",
        "approve-item": "/<pid_value>/<feedback_id>/actions/approve"
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


__all__ = (
    "UserFeedbackResourceConfig"
)
