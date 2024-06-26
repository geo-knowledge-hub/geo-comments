# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""GEO Comments contrib module to support feedback in the Marketplace API."""

from .resource import (
    MarketplaceItemFeedbackResource,
    MarketplaceItemFeedbackResourceConfig,
)
from .service import (
    MarketplaceItemFeedbackService,
    MarketplaceItemFeedbackServiceConfig,
)

__all__ = (
    "MarketplaceItemFeedbackResource",
    "MarketplaceItemFeedbackResourceConfig",
    "MarketplaceItemFeedbackService",
    "MarketplaceItemFeedbackServiceConfig",
)
