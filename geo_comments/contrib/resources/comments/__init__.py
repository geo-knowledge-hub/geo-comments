# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""GEO Comments contrib module to support comments in the Records API."""

from .resource import ResourceCommentResource, ResourceCommentResourceConfig
from .service import ResourceCommentService, ResourceCommentServiceConfig

__all__ = (
    "ResourceCommentResource",
    "ResourceCommentResourceConfig",
    "ResourceCommentService",
    "ResourceCommentServiceConfig",
)
