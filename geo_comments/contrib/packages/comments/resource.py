# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resource for the Packages API contrib."""

from ..packages import package_comments

#
# Resource
#
PackageCommentResource = package_comments.resource_cls

#
# Configuration
#
PackageCommentResourceConfig = package_comments.resource_config_cls
