# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Contrib - comments and feedback for Marketplace Items API."""

from geo_rdm_records.modules.marketplace.records.api import GEOMarketplaceItem
from geo_rdm_records.modules.marketplace.records.models import (
    GEOMarketplaceItemMetadata,
)

from geo_comments.factories import CommentTypeFactory, FeedbackTypeFactory

from .systemfield import RecordEntity

#
# Comment
#
marketplace_comments = CommentTypeFactory(
    comment_type_name="MarketplaceComment",
    comment_record_type_name="marketplace-item",
    comment_record_entity_cls=RecordEntity,
    comment_associated_record_cls=GEOMarketplaceItem,
    comment_associated_metadata_cls=GEOMarketplaceItemMetadata,
    comment_service_id="marketplace_item_comments",
    comment_service_name="MarketplaceItemComments",
    comment_service_endpoint_route="/comments",
    comment_service_endpoint_route_prefix="/marketplace/items",
)

#
# Feedback
#
marketplace_feedback = FeedbackTypeFactory(
    comment_type_name="MarketplaceFeedback",
    comment_record_type_name="marketplace-item",
    comment_record_entity_cls=RecordEntity,
    comment_associated_record_cls=GEOMarketplaceItem,
    comment_associated_metadata_cls=GEOMarketplaceItemMetadata,
    comment_service_id="marketplace_item_feedback",
    comment_service_name="MarketplaceItemFeedback",
    comment_service_endpoint_route="/feedback",
    comment_service_endpoint_route_prefix="/marketplace/items",
)
