# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from flask import g, current_app
from flask_resources import (
    route,
    response_handler,
    resource_requestctx,
    create_error_handler,
    Resource,
    HTTPJSONException,
)

from sqlalchemy.exc import IntegrityError

from invenio_records_resources.resources.errors import ErrorHandlersMixin
from invenio_records_resources.resources.records.utils import es_preference


from geo_feedback.feedback.resources.parser import (
    request_data,
    request_headers,
    request_read_args,
    request_search_args,
    request_feedback_view_args,
)


class FeedbackErrorHandlersMixin:
    """Error mixin handler for Feedback Resources classes."""

    error_handlers = {
        **ErrorHandlersMixin.error_handlers,
        IntegrityError: create_error_handler(
            HTTPJSONException(
                code=409,
                description="User have already created feedback for this record.",
            )
        ),
    }


class FeedbackResource(FeedbackErrorHandlersMixin, Resource):
    """Record resource."""

    def __init__(self, config, service):
        """Constructor."""
        super(FeedbackResource, self).__init__(config)
        self.service = service

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes
        return [
            # General routes
            route("GET", routes["list"], self.search),
            route("POST", routes["list"], self.create),
            route("PUT", routes["item"], self.update),
            route("DELETE", routes["item"], self.delete),
            route("GET", routes["item"], self.read),
            # Admin routes
            route("POST", routes["deny-item"], self.deny_feedback),
            route("POST", routes["allow-item"], self.allow_feedback),
        ]

    @request_search_args
    @response_handler(many=True)
    def search(self):
        """Perform a search over the items."""
        hits = self.service.search(
            identity=g.identity,
            params=resource_requestctx.args,
            es_preference=es_preference(),
        )
        return hits.to_dict(), 200

    @request_feedback_view_args
    @response_handler(many=False)
    def read(self):
        """Read an item."""
        item = self.service.read(
            g.identity,
            feedback_id=resource_requestctx.view_args["fid"],
        )

        return item.to_dict(), 200

    @request_data
    @response_handler()
    def create(self):
        """Create an item."""
        item = self.service.create(
            g.identity,
            resource_requestctx.data or {},
            auto_approve=current_app.config.get("GEO_FEEDBACK_AUTO_APPROVE", False),
        )
        return item.to_dict(), 201

    @request_headers
    @request_feedback_view_args
    @request_data
    @response_handler()
    def update(self):
        """Update an item."""
        item = self.service.update(
            identity=g.identity,
            feedback_id=resource_requestctx.view_args["fid"],
            data=resource_requestctx.data,
        )
        return item.to_dict(), 200

    @request_feedback_view_args
    def delete(self):
        """Delete an item."""
        self.service.delete(
            identity=g.identity, feedback_id=resource_requestctx.view_args["fid"]
        )
        return "", 204

    @request_headers
    @request_read_args
    @request_feedback_view_args
    def deny_feedback(self):
        denied_feedback = self.service.deny_feedback(
            identity=g.identity, feedback_id=resource_requestctx.view_args["fid"]
        )

        return denied_feedback.to_dict(), 200

    @request_headers
    @request_read_args
    @request_feedback_view_args
    def allow_feedback(self):
        allowed_feedback = self.service.allow_feedback(
            identity=g.identity, feedback_id=resource_requestctx.view_args["fid"]
        )

        return allowed_feedback.to_dict(), 200
