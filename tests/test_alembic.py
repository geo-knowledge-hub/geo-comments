# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 GEO Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test alembic recipes for GEO-Comments."""

import pytest
from invenio_db.utils import alembic_test_context, drop_alembic_version_table


def test_alembic(base_app, database):
    """Test alembic recipes."""
    db = database
    ext = base_app.extensions["invenio-db"]

    if db.engine.name == "sqlite":
        raise pytest.skip("Upgrades are not supported on SQLite.")

    base_app.config["ALEMBIC_CONTEXT"] = alembic_test_context()

    # Check that this package's SQLAlchemy models have been properly registered
    tables = [x.name for x in db.get_tables_for_bind()]
    assert "packagecomment_metadata" in tables
    assert "packagefeedback_metadata" in tables
    assert "resourcecomment_metadata" in tables
    assert "resourcefeedback_metadata" in tables

    # Check that Alembic agrees that there's no further tables to create.
    assert not ext.alembic.compare_metadata()

    # Drop everything and recreate tables all with Alembic
    db.drop_all()
    drop_alembic_version_table()
    ext.alembic.upgrade()
    assert not ext.alembic.compare_metadata()

    # Try to upgrade and downgrade
    ext.alembic.stamp()
    ext.alembic.downgrade(target="96e796392533")
    ext.alembic.upgrade()
    assert not ext.alembic.compare_metadata()

    drop_alembic_version_table()
