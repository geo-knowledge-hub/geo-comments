# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment resource."""

from flask import current_app, g
from flask_resources import (
    HTTPJSONException,
    Resource,
    create_error_handler,
    resource_requestctx,
    response_handler,
    route,
)
from invenio_records_resources.resources.errors import ErrorHandlersMixin
from invenio_records_resources.resources.records.utils import es_preference
from sqlalchemy.exc import IntegrityError

from geo_comments.comments.resources.parser import (
    request_comment_view_args,
    request_data,
    request_headers,
    request_read_args,
    request_search_args,
)


class CommentErrorHandlersMixin:
    """Error mixin handler for Comment Resources classes."""

    error_handlers = {
        **ErrorHandlersMixin.error_handlers,
        IntegrityError: create_error_handler(
            HTTPJSONException(
                code=409,
                description="User have already created comment for this record.",
            )
        ),
    }


class CommentResource(CommentErrorHandlersMixin, Resource):
    """Record resource."""

    def __init__(self, config, service):
        """Constructor."""
        super(CommentResource, self).__init__(config)
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
            route("POST", routes["deny-item"], self.deny_comment),
            route("POST", routes["allow-item"], self.allow_comment),
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

    @request_comment_view_args
    @response_handler(many=False)
    def read(self):
        """Read an item."""
        item = self.service.read(
            g.identity,
            comment_id=resource_requestctx.view_args["fid"],
        )

        return item.to_dict(), 200

    @request_data
    @response_handler()
    def create(self):
        """Create an item."""
        item = self.service.create(
            g.identity,
            resource_requestctx.data or {},
            auto_approve=current_app.config.get("GEO_COMMENT_AUTO_APPROVE", False),
        )
        return item.to_dict(), 201

    @request_headers
    @request_comment_view_args
    @request_data
    @response_handler()
    def update(self):
        """Update an item."""
        item = self.service.update(
            identity=g.identity,
            comment_id=resource_requestctx.view_args["fid"],
            data=resource_requestctx.data,
        )
        return item.to_dict(), 200

    @request_comment_view_args
    def delete(self):
        """Delete an item."""
        self.service.delete(
            identity=g.identity, comment_id=resource_requestctx.view_args["fid"]
        )
        return "", 204

    @request_headers
    @request_read_args
    @request_comment_view_args
    def deny_comment(self):
        """Deny comment."""
        denied_comment = self.service.deny_comment(
            identity=g.identity, comment_id=resource_requestctx.view_args["fid"]
        )

        return denied_comment.to_dict(), 200

    @request_headers
    @request_read_args
    @request_comment_view_args
    def allow_comment(self):
        """Allow comment."""
        allowed_comment = self.service.allow_comment(
            identity=g.identity, comment_id=resource_requestctx.view_args["fid"]
        )

        return allowed_comment.to_dict(), 200
