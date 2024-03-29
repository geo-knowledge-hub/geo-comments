# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""GEO Comments contrib module to support feedback in the Packages API."""

from .resource import PackageFeedbackResource, PackageFeedbackResourceConfig
from .service import PackageFeedbackService, PackageFeedbackServiceConfig

__all__ = (
    "PackageFeedbackResource",
    "PackageFeedbackResourceConfig",
    "PackageFeedbackService",
    "PackageFeedbackServiceConfig",
)
