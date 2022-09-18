# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Contrib module test."""

import pytest
from geo_rdm_records.customizations.records.api import GEODraft, GEORecord
from geo_rdm_records.modules.packages.records.api import (
    GEOPackageDraft,
    GEOPackageRecord,
)
from invenio_app.factory import create_api
from invenio_db import db


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return create_api


@pytest.fixture(scope="module")
def record_resource_simple(minimal_record, location, resource_type_v):
    """Basic Resource Record."""
    draft = GEODraft.create(minimal_record)
    draft.commit()
    db.session.commit()

    record = GEORecord.publish(draft)
    record.commit()
    db.session.commit()

    GEODraft.index.refresh()
    GEORecord.index.refresh()

    return record


@pytest.fixture(scope="module")
def record_package_simple(minimal_record, location, resource_type_v):
    """Basic Package Record."""
    draft = GEOPackageDraft.create(minimal_record)
    draft.commit()
    db.session.commit()

    record = GEOPackageRecord.publish(draft)
    record.commit()
    db.session.commit()

    GEOPackageDraft.index.refresh()
    GEOPackageRecord.index.refresh()

    return record
