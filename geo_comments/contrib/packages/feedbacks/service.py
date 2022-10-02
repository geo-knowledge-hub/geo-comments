# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service for the Packages API contrib."""

from ..packages import package_feedbacks
from .schema import FeedbackCommentSchema

#
# Service
#
PackageFeedbackService = package_feedbacks.comment_service_cls


#
# Configuration
#
class PackageFeedbackServiceConfig(package_feedbacks.comment_service_cls_config):
    """Service configuration class."""

    schema = FeedbackCommentSchema
