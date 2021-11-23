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
    Resource, route, response_handler, resource_requestctx
)

from invenio_records_resources.resources.errors import ErrorHandlersMixin

from .parser import request_view_args, request_data, request_search_args

from ..records.models import FeedbackStatus


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
            route("POST", routes["allow-item"], self.allow_feedback)
        ]

    @request_data
    @request_view_args
    @response_handler()
    def create_feedback(self):
        created_feedback = self.service.create_feedback(
            g.identity,
            resource_requestctx.view_args["recid"],
            resource_requestctx.data,
            auto_approve=current_app.config.get("GEO_FEEDBACK_AUTO_APPROVE", False)
        )

        return created_feedback.to_dict(), 201

    @request_view_args
    @response_handler()
    def get_feedback(self):
        selected_feedback = self.service.get_feedback(
            g.identity,
            resource_requestctx.view_args["feedback_id"]
        )

        return selected_feedback.to_dict(), 200

    @request_data
    @request_view_args
    @response_handler()
    def edit_feedback(self):
        feedback_edited = self.service.edit_feedback(
            g.identity,
            resource_requestctx.view_args["feedback_id"],
            resource_requestctx.data
        )

        return feedback_edited.to_dict(), 200

    @request_view_args
    @response_handler(many=True)
    def list_feedback_by_record(self):
        selected_feedbacks = self.service.list_record_feedback(
            g.identity,
            status=FeedbackStatus.ALLOWED.value,
            is_deleted=False,
            recid=resource_requestctx.view_args["recid"]
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
            resource_requestctx.view_args["feedback_id"]
        )

        return '', 204

    @request_view_args
    def deny_feedback(self):
        denied_feedback = self.service.deny_feedback(
            g.identity,
            resource_requestctx.view_args["feedback_id"]
        )

        return denied_feedback.to_dict(), 200

    @request_view_args
    def allow_feedback(self):
        allowed_feedback = self.service.allow_feedback(
            g.identity,
            resource_requestctx.view_args["feedback_id"]
        )

        return allowed_feedback.to_dict(), 200


__all__ = (
    "UserFeedbackResource"
)
