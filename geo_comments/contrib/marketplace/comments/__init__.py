# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""GEO Comments contrib module to support comments in the Marketplace API."""

from .resource import (
    MarketplaceItemCommentResource,
    MarketplaceItemCommentResourceConfig,
)
from .service import MarketplaceItemCommentService, MarketplaceItemCommentServiceConfig

__all__ = (
    "MarketplaceItemCommentResource",
    "MarketplaceItemCommentResourceConfig",
    "MarketplaceItemCommentService",
    "MarketplaceItemCommentServiceConfig",
)
