# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Contrib - System field for packages comments and feedbacks."""

from geo_rdm_records.modules.packages.records.api import GEOPackageRecord

from geo_comments.comments.records.systemfields.models import BaseRecordEntity


class RecordEntity(BaseRecordEntity):
    """Record entity abstraction class (for Packages)."""

    entity_cls = GEOPackageRecord
    """Record entity class."""
