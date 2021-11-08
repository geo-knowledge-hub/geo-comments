# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Feedback module for Geo Knowledge Hub"""

from flask_babelex import gettext as _

from . import config
from .feedback.resources.config import UserFeedbackResourceConfig
from .feedback.resources.resource import UserFeedbackResource
from .feedback.services.config import FeedbackServiceConfig
from .feedback.services.service import UserFeedbackService


class GEOFeedback(object):
    """geo-feedback extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['geo-feedback'] = self

        self.init_services(app)
        self.init_resources(app)

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith('GEO_FEEDBACK_'):
                app.config.setdefault(k, getattr(config, k))

    def init_services(self, app):
        self.service = UserFeedbackService(FeedbackServiceConfig)

    def init_resources(self, app):
        self.feedback_resource = UserFeedbackResource(
            UserFeedbackResourceConfig,
            self.service
        )
