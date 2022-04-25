# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Feedback module for GEO Knowledge Hub"""

from geo_feedback import config

from geo_feedback.feedback.resources.config import FeedbackResourceConfig

from geo_feedback.feedback.resources.resource import FeedbackResource

from geo_feedback.feedback.services.config import FeedbackServiceConfig
from geo_feedback.feedback.services.services import FeedbackService


class GEOFeedback(object):
    """geo-feedback extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["geo-feedback"] = self

        self.init_services(app)
        self.init_resources(app)

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("GEO_FEEDBACK_"):
                app.config.setdefault(k, getattr(config, k))

    def init_services(self, app):
        """Initialize the services."""

        self.feedback_service = FeedbackService(config=FeedbackServiceConfig)

    def init_resources(self, app):
        """Initialize the resources."""
        self.feedback_resource = FeedbackResource(
            FeedbackResourceConfig, self.feedback_service
        )
