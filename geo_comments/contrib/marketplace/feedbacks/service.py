# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service for the Marketplace Item API contrib."""

from ..marketplace import marketplace_feedback
from .schema import FeedbackCommentSchema

#
# Service
#
MarketplaceItemFeedbackService = marketplace_feedback.comment_service_cls


#
# Configuration
#
class MarketplaceItemFeedbackServiceConfig(
    marketplace_feedback.comment_service_cls_config
):
    """Service configuration class."""

    schema = FeedbackCommentSchema
