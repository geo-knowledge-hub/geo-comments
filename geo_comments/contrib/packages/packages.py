# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Contrib - comments and feedbacks for Packages API."""

from geo_rdm_records.modules.packages.records.models import GEOPackageRecordMetadata

from geo_comments.comments.records.systemfields.models import RecordEntity
from geo_comments.factories import CommentTypeFactory, FeedbackTypeFactory

#
# Comment
#
package_comments = CommentTypeFactory(
    comment_type_name="PackageComment",
    comment_record_entity_cls=RecordEntity,
    comment_associated_record_cls=GEOPackageRecordMetadata,
)

#
# Feedbacks
#
package_feedbacks = FeedbackTypeFactory(
    comment_type_name="PackageFeedback",
    comment_record_entity_cls=RecordEntity,
    comment_associated_record_cls=GEOPackageRecordMetadata,
)
