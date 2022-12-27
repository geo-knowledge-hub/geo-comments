# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Contrib - comments and feedbacks for Packages API."""

from geo_rdm_records.customizations.records.api import GEORecord
from invenio_rdm_records.records.models import RDMRecordMetadata as GEORecordMetadata

from geo_comments.factories import CommentTypeFactory, FeedbackTypeFactory

from .systemfield import RecordEntity

#
# Comment
#
resource_comments = CommentTypeFactory(
    comment_type_name="ResourceComment",
    comment_record_entity_cls=RecordEntity,
    comment_associated_record_cls=GEORecord,
    comment_associated_metadata_cls=GEORecordMetadata,
    comment_service_id="resource_comment",
    comment_service_name="ResourceComment",
    comment_service_endpoint_route="/comments",
    comment_service_endpoint_route_prefix="/records",
)

#
# Feedbacks
#
resource_feedbacks = FeedbackTypeFactory(
    comment_type_name="ResourceFeedback",
    comment_record_entity_cls=RecordEntity,
    comment_associated_record_cls=GEORecord,
    comment_associated_metadata_cls=GEORecordMetadata,
    comment_service_id="resource_feedback",
    comment_service_name="ResourceFeedback",
    comment_service_endpoint_route="/feedback",
    comment_service_endpoint_route_prefix="/records",
)
