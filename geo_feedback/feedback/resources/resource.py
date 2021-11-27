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
    Resource
)

from invenio_records_resources.resources.errors import ErrorHandlersMixin

from .parser import (
    request_data,
    request_record_args,
    request_search_args,
    request_feedback_args
)


class UserFeedbackResource(ErrorHandlersMixin, Resource):

    def __init__(self, config, service):
        super(UserFeedbackResource, self).__init__(config)

        self.service = service

    def create_url_rules(self):
        routes = self.config.routes
        return [
            # General routes
            route("GET", routes["base"], self.search_feedback),
            route("PUT", routes["base"], self.update_feedback),
            route("POST", routes["base"], self.create_feedback),
            route("DELETE", routes["base"], self.delete_feedback),

            # Admin routes
            route("POST", routes["deny-item"], self.deny_feedback),
            route("POST", routes["allow-item"], self.allow_feedback)
        ]

    @request_data
    @request_record_args
    @response_handler()
    def create_feedback(self):
        created_feedback = self.service.create_feedback(
            g.identity,
            resource_requestctx.args["recid"],
            resource_requestctx.data,
            auto_approve=current_app.config.get("GEO_FEEDBACK_AUTO_APPROVE", False)
        )

        return created_feedback.to_dict(), 201

    @request_search_args
    @response_handler(many=True)
    def search_feedback(self):
        selected_feedbacks = self.service.search_record_feedback(g.identity, **resource_requestctx.args)

        return [sfeedback.to_dict() for sfeedback in selected_feedbacks], 200

    @request_data
    @request_feedback_args
    @response_handler()
    def update_feedback(self):
        feedback_edited = self.service.edit_feedback(
            g.identity,
            resource_requestctx.args["id"],
            resource_requestctx.data
        )

        return feedback_edited.to_dict(), 200

    @request_feedback_args
    def delete_feedback(self):
        self.service.delete_feedback(
            g.identity,
            resource_requestctx.args["id"]
        )

        return '', 204

    @request_feedback_args
    def deny_feedback(self):
        denied_feedback = self.service.deny_feedback(
            g.identity,
            resource_requestctx.args["id"]
        )

        return denied_feedback.to_dict(), 200

    @request_feedback_args
    def allow_feedback(self):
        allowed_feedback = self.service.allow_feedback(
            g.identity,
            resource_requestctx.args["id"]
        )

        return allowed_feedback.to_dict(), 200


__all__ = (
    "UserFeedbackResource"
)
