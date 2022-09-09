# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Factory tests."""

import pytest

from geo_comments.factories import CommentTypeFactory, FeedbackTypeFactory
from geo_comments.comments.records.systemfields.models import RecordEntity

from geo_rdm_records.modules.packages.records.models import GEOPackageRecordMetadata
from invenio_rdm_records.records.models import RDMRecordMetadata as GEORecordMetadata


def test_feedback_model_class_create():
    """Test the creation of a modal class."""
    # Packages
    package_feedbacks = FeedbackTypeFactory(
        comment_type_name="PackageFeedbackTest",
        comment_record_entity_cls=RecordEntity,
        comment_associated_record_cls=GEOPackageRecordMetadata,
    )

    assert package_feedbacks.model_cls.__name__ == "PackageFeedbackTestMetadata"
    assert package_feedbacks.model_cls.__tablename__ == "packagefeedbacktest_metadata"

    # Resources
    resource_feedbacks = FeedbackTypeFactory(
        comment_type_name="ResourceFeedbackTest",
        comment_record_entity_cls=RecordEntity,
        comment_associated_record_cls=GEORecordMetadata,
    )

    assert resource_feedbacks.model_cls.__name__ == "ResourceFeedbackTestMetadata"
    assert resource_feedbacks.model_cls.__tablename__ == "resourcefeedbacktest_metadata"
