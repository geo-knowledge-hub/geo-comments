# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resource for the Packages API contrib."""

from ..packages import package_feedbacks

#
# Resource
#
PackageFeedbackResource = package_feedbacks.resource_cls

#
# Configuration
#
PackageFeedbackResourceConfig = package_feedbacks.resource_config_cls
