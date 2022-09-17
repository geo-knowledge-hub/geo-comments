# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""GEO Comments contrib module to support feedback in the Records API."""

from .resource import ResourceFeedbackResource, ResourceFeedbackResourceConfig
from .service import ResourceFeedbackService, ResourceFeedbackServiceConfig

__all__ = (
    "ResourceFeedbackResource",
    "ResourceFeedbackResourceConfig",
    "ResourceFeedbackService",
    "ResourceFeedbackServiceConfig",
)
