# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Factories test configuration."""

import pytest
from invenio_app.factory import create_api as _create_api
from invenio_rdm_records.records.api import RDMRecord

from geo_comments.comments.records.systemfields.models import BaseRecordEntity


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return _create_api


@pytest.fixture()
def record_entity():
    """Generic Record entity fixture."""

    class TestRecordEntity(BaseRecordEntity):
        entity_cls = RDMRecord

    return TestRecordEntity
