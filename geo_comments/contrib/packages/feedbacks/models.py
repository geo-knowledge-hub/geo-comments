# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Data Model for the Packages API contrib."""

from ..packages import package_feedbacks

PackageFeedbackMetadata = package_feedbacks.model_cls
