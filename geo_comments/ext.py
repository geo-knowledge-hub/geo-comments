# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comments module for GEO Knowledge Hub."""

from geo_comments import config
from geo_comments.contrib.marketplace.comments import (
    MarketplaceItemCommentResource,
    MarketplaceItemCommentResourceConfig,
    MarketplaceItemCommentService,
    MarketplaceItemCommentServiceConfig,
)
from geo_comments.contrib.marketplace.feedbacks import (
    MarketplaceItemFeedbackResource,
    MarketplaceItemFeedbackResourceConfig,
    MarketplaceItemFeedbackService,
    MarketplaceItemFeedbackServiceConfig,
)
from geo_comments.contrib.packages.comments import (
    PackageCommentResource,
    PackageCommentResourceConfig,
    PackageCommentService,
    PackageCommentServiceConfig,
)
from geo_comments.contrib.packages.feedbacks import (
    PackageFeedbackResource,
    PackageFeedbackResourceConfig,
    PackageFeedbackService,
    PackageFeedbackServiceConfig,
)
from geo_comments.contrib.resources.comments import (
    ResourceCommentResource,
    ResourceCommentResourceConfig,
    ResourceCommentService,
    ResourceCommentServiceConfig,
)
from geo_comments.contrib.resources.feedbacks import (
    ResourceFeedbackResource,
    ResourceFeedbackResourceConfig,
    ResourceFeedbackService,
    ResourceFeedbackServiceConfig,
)


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
        self.package_comment_service = PackageCommentService(
            config=PackageCommentServiceConfig
        )
        self.package_feedback_service = PackageFeedbackService(
            config=PackageFeedbackServiceConfig
        )

        self.resource_comment_service = ResourceCommentService(
            config=ResourceCommentServiceConfig
        )
        self.resource_feedback_service = ResourceFeedbackService(
            config=ResourceFeedbackServiceConfig
        )

        self.marketplace_item_comment_service = MarketplaceItemCommentService(
            config=MarketplaceItemCommentServiceConfig
        )
        self.marketplace_item_feedback_service = MarketplaceItemFeedbackService(
            config=MarketplaceItemFeedbackServiceConfig
        )

    def init_resources(self, app):
        """Initialize the resources."""
        self.package_comment_resource = PackageCommentResource(
            service=self.package_comment_service, config=PackageCommentResourceConfig
        )
        self.package_feedback_resource = PackageFeedbackResource(
            service=self.package_feedback_service, config=PackageFeedbackResourceConfig
        )

        self.resource_comment_resource = ResourceCommentResource(
            service=self.resource_comment_service, config=ResourceCommentResourceConfig
        )
        self.resource_feedback_resource = ResourceFeedbackResource(
            service=self.resource_feedback_service,
            config=ResourceFeedbackResourceConfig,
        )

        self.marketplace_item_comment_resource = MarketplaceItemCommentResource(
            service=self.marketplace_item_comment_service,
            config=MarketplaceItemCommentResourceConfig,
        )
        self.marketplace_item_feedback_resource = MarketplaceItemFeedbackResource(
            service=self.marketplace_item_feedback_service,
            config=MarketplaceItemFeedbackResourceConfig,
        )
