# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service for the Marketplace Item API contrib."""

from ..marketplace import marketplace_comments
from .schema import CommentSchema

#
# Service
#
MarketplaceItemCommentService = marketplace_comments.comment_service_cls


#
# Configuration
#
class MarketplaceItemCommentServiceConfig(
    marketplace_comments.comment_service_cls_config
):
    """Service configuration class."""

    schema = CommentSchema
