# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Factory tests."""

import pytest
from geo_rdm_records.modules.packages import GEOPackageRecord
from geo_rdm_records.modules.packages.records.models import GEOPackageRecordMetadata
from invenio_rdm_records.records.models import RDMRecordMetadata as GEORecordMetadata

from geo_comments.factories import CommentTypeFactory, FeedbackTypeFactory


@pytest.mark.parametrize(
    "type_factory,type_name",
    [
        (FeedbackTypeFactory, "ModelFeedbackTest"),
        (CommentTypeFactory, "ModelCommentTest"),
    ],
)
def test_model_class_create(type_factory, type_name, record_entity):
    """Test the creation of a modal class."""
    # Packages
    type_name_ = type_name

    type_name = f"Package{type_name_}"
    type_expected = f"{type_name}Metadata"
    type_table_expected = f"{type_name.lower()}_metadata"

    package_feedbacks = type_factory(
        comment_type_name=type_name,
        comment_record_type_name=type_name,
        comment_record_entity_cls=record_entity,
        comment_associated_record_cls=GEOPackageRecord,
        comment_associated_metadata_cls=GEOPackageRecordMetadata,
    )

    assert package_feedbacks.model_cls.__name__ == type_expected
    assert package_feedbacks.model_cls.__tablename__ == type_table_expected

    # Resources
    type_name = f"Resource{type_name_}"
    type_expected = f"{type_name}Metadata"
    type_table_expected = f"{type_name.lower()}_metadata"

    resource_feedbacks = type_factory(
        comment_type_name=type_name,
        comment_record_type_name=type_name,
        comment_record_entity_cls=record_entity,
        comment_associated_record_cls=GEOPackageRecord,
        comment_associated_metadata_cls=GEOPackageRecordMetadata,
    )

    assert resource_feedbacks.model_cls.__name__ == type_expected
    assert resource_feedbacks.model_cls.__tablename__ == type_table_expected
