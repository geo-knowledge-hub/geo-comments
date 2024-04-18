# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Contrib - System field for marketplace comments and feedback."""

from geo_rdm_records.modules.marketplace.records.api import GEOMarketplaceItem

from geo_comments.comments.records.systemfields.models import BaseRecordEntity


class RecordEntity(BaseRecordEntity):
    """Record entity abstraction class (for Marketplace Items)."""

    entity_cls = GEOMarketplaceItem
    """Record entity class."""
