# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resource for the Marketplace Items API contrib."""

from ..marketplace import marketplace_feedback

#
# Resource
#
MarketplaceItemFeedbackResource = marketplace_feedback.resource_cls

#
# Configuration
#
MarketplaceItemFeedbackResourceConfig = marketplace_feedback.resource_config_cls
