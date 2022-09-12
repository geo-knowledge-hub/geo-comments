# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comments module for GEO Knowledge Hub."""

from geo_comments import config
from geo_comments.comments.resources.config import (
    CommentResourceConfig,
    FeedbackResourceConfig,
)
from geo_comments.comments.resources.resource import CommentResource
from geo_comments.comments.services.config import (
    CommentServiceConfig,
    FeedbackServiceConfig,
)
from geo_comments.comments.services.services import CommentService


class GEOComments(object):
    """geo-comments extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["geo-comments"] = self

        self.init_services(app)
        self.init_resources(app)

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("GEO_COMMENTS_"):
                app.config.setdefault(k, getattr(config, k))

    def init_services(self, app):
        """Initialize the services."""
        self.comments_service = CommentService(config=CommentServiceConfig)
        self.feedbacks_service = CommentService(config=FeedbackServiceConfig)

    def init_resources(self, app):
        """Initialize the resources."""
        self.comments_resource = CommentResource(
            CommentResourceConfig, self.comments_service
        )

        self.feedbacks_resource = CommentResource(
            FeedbackResourceConfig, self.feedbacks_service
        )
