# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Contrib - comments and feedbacks for Packages API."""

from geo_rdm_records.modules.packages.records.api import GEOPackageRecord
from geo_rdm_records.modules.packages.records.models import GEOPackageRecordMetadata

from geo_comments.factories import CommentTypeFactory, FeedbackTypeFactory

from .systemfield import RecordEntity

#
# Comment
#
package_comments = CommentTypeFactory(
    comment_type_name="PackageComment",
    comment_record_entity_cls=RecordEntity,
    comment_associated_record_cls=GEOPackageRecord,
    comment_associated_metadata_cls=GEOPackageRecordMetadata,
    comment_service_id="package_comments",
    comment_service_name="PackageComments",
    comment_service_endpoint_route="/comments",
    comment_service_endpoint_route_prefix="/packages",
)

#
# Feedbacks
#
package_feedbacks = FeedbackTypeFactory(
    comment_type_name="PackageFeedback",
    comment_record_entity_cls=RecordEntity,
    comment_associated_record_cls=GEOPackageRecord,
    comment_associated_metadata_cls=GEOPackageRecordMetadata,
    comment_service_id="package_feedback",
    comment_service_name="PackageFeedback",
    comment_service_endpoint_route="/feedbacks",
    comment_service_endpoint_route_prefix="/packages",
)
