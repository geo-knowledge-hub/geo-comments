# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from flask import g, current_app

from flask_resources import (
    Resource, route, response_handler, resource_requestctx
)

from .parser import request_view_args, request_data, request_search_args

from invenio_records_resources.resources.errors import ErrorHandlersMixin


class UserFeedbackResource(ErrorHandlersMixin, Resource):

    def __init__(self, config, service):
        super(UserFeedbackResource, self).__init__(config)

        self.service = service

    def create_url_rules(self):
        routes = self.config.routes
        return [
            # General routes
            route("GET", routes["get-item"], self.get_feedback),
            route("PUT", routes["update-item"], self.edit_feedback),
            route("POST", routes["create-item"], self.create_feedback),
            route("DELETE", routes["delete-item"], self.delete_feedback),
            route("GET", routes["list-item"], self.list_feedback_by_record),

            # Admin routes
            route("GET", routes["search-item"], self.search_feedback),

            route("POST", routes["deny-item"], self.deny_feedback),
            route("POST", routes["approve-item"], self.approve_feedback)
        ]

    @request_data
    @request_view_args
    @response_handler()
    def create_feedback(self):
        created_feedback = self.service.create_feedback(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.data,
            auto_approve=current_app.config.get("GEO_FEEDBACK_AUTO_APPROVE", False)
        )

        return created_feedback.to_dict(), 201

    @request_view_args
    @response_handler()
    def get_feedback(self):
        selected_feedback = self.service.get_feedback(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.view_args["feedback_id"]
        )

        return selected_feedback.to_dict(), 200

    @request_data
    @request_view_args
    @response_handler()
    def edit_feedback(self):
        feedback_edited = self.service.edit_feedback(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.view_args["feedback_id"],
            resource_requestctx.data
        )

        return feedback_edited.to_dict(), 200

    @request_view_args
    @response_handler(many=True)
    def list_feedback_by_record(self):
        selected_feedbacks = self.service.list_record_feedback(
            g.identity,
            is_deleted=False,
            is_approved=True,
            pid_value=resource_requestctx.view_args["pid_value"]
        )

        return [sfeedback.to_dict() for sfeedback in selected_feedbacks], 200

    @request_view_args
    @request_search_args
    @response_handler(many=True)
    def search_feedback(self):
        selected_feedbacks = self.service.search_record_feedback(g.identity, **resource_requestctx.args)

        return [sfeedback.to_dict() for sfeedback in selected_feedbacks], 200

    @request_view_args
    def delete_feedback(self):
        self.service.delete_feedback(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.view_args["feedback_id"]
        )

        return '', 204

    @request_view_args
    def deny_feedback(self):
        denied_feedback = self.service.deny_feedback(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.view_args["feedback_id"]
        )

        return denied_feedback.to_dict(), 200

    @request_view_args
    def approve_feedback(self):
        approved_feedback = self.service.approve_feedback(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.view_args["feedback_id"]
        )

        return approved_feedback.to_dict(), 200


__all__ = (
    "UserFeedbackResource"
)
