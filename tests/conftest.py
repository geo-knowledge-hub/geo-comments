# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""GEO Comments test configuration."""

import pytest
from flask_principal import Identity, Need, UserNeed
from flask_security import login_user
from flask_security.utils import hash_password
from geo_rdm_records.modules.packages.records.api import (
    GEOPackageDraft,
    GEOPackageRecord,
)
from geo_rdm_records.modules.resources.records.api import GEODraft, GEORecord
from invenio_access.models import ActionRoles
from invenio_access.permissions import superuser_access
from invenio_accounts.models import Role
from invenio_accounts.testutils import login_user_via_session
from invenio_app.factory import create_api as _create_api


#
# Flask application
#
def _(x):
    """Identity function for string extraction."""
    return x


@pytest.fixture(scope="module")
def celery_config():
    """Override pytest-invenio fixture."""
    return {}


@pytest.fixture(scope="module")
def app_config(app_config):
    """Mimic an instance's configuration."""
    app_config["JSONSCHEMAS_HOST"] = "localhost"

    app_config[
        "RECORDS_REFRESOLVER_CLS"
    ] = "invenio_records.resolver.InvenioRefResolver"

    app_config[
        "RECORDS_REFRESOLVER_STORE"
    ] = "invenio_jsonschemas.proxies.current_refresolver_store"

    return app_config


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return _create_api


#
# Identity
#
@pytest.fixture(scope="module")
def identity_simple():
    """Simple identity fixture."""
    i = Identity(1)
    i.provides.add(UserNeed(1))
    i.provides.add(Need(method="system_role", value="any_user"))
    i.provides.add(Need(method="system_role", value="authenticated_user"))
    return i


#
# Users
#
@pytest.fixture(scope="module")
def users(app):
    """Create example users."""
    # This is a convenient way to get a handle on db that, as opposed to the
    # fixture, won't cause a DB rollback after the test is run in order
    # to help with test performance (creating users is a module -if not higher-
    # concern)
    from invenio_db import db

    with db.session.begin_nested():
        datastore = app.extensions["security"].datastore

        su_role = Role(name="superuser-access")
        db.session.add(su_role)

        su_action_role = ActionRoles.create(action=superuser_access, role=su_role)
        db.session.add(su_action_role)

        user1 = datastore.create_user(
            email="user1@example.org", password=hash_password("password"), active=True
        )
        user2 = datastore.create_user(
            email="user2@example.org", password=hash_password("password"), active=True
        )
        admin = datastore.create_user(
            email="admin@example.org", password=hash_password("password"), active=True
        )
        admin.roles.append(su_role)

    db.session.commit()
    return [user1, user2, admin]


#
# Service client
#
@pytest.fixture()
def client_logged_as(client, users):
    """Logs in a user to the client."""

    def log_user(user_email):
        """Log the user."""
        user = next((u for u in users if u.email == user_email), None)
        login_user(user, remember=True)
        login_user_via_session(client, email=user_email)
        return client

    return log_user


#
# Data Layer fixtures
#
@pytest.fixture(scope="module")
def comment_record_data():
    """Data to create a comment."""
    return {
        "comment": "A comment here",
        "topics": [
            {"name": "Test A", "rating": 12.4},
            {"name": "Test B", "rating": 15.5},
        ],
    }


#
# Data fixtures
#
@pytest.fixture(scope="module")
def minimal_record():
    """Minimal record data as dict coming from the external world."""
    return {
        "pids": {},
        "access": {
            "record": "public",
            "files": "public",
        },
        "files": {
            "enabled": False,  # Most tests don't care about files
        },
        "metadata": {
            "target_audiences": [{"id": "tu-geo-eoanalyst"}],
            "engagement_priorities": [
                {
                    "id": "convention-on-biological-diversity",
                }
            ],
            "geo_work_programme_activity": {
                "id": "geo-activities-geobon",
            },
            "publication_date": "2020-06-01",
            "resource_type": {"id": "image-photo"},
            "creators": [
                {
                    "person_or_org": {
                        "family_name": "Brown",
                        "given_name": "Troy",
                        "type": "personal",
                    }
                },
                {
                    "person_or_org": {
                        "name": "Troy Inc.",
                        "type": "organizational",
                    },
                },
            ],
            "title": "A Romans story",
        },
    }


@pytest.fixture(scope="module")
def record_rdm_simple(minimal_record):
    """Basic RDM Record."""
    draft = GEODraft.create(minimal_record)
    record = GEORecord.publish(draft)

    return record


@pytest.fixture(scope="module")
def record_package_simple(minimal_record):
    """Basic Package Record."""
    draft = GEOPackageDraft.create(minimal_record)
    record = GEOPackageRecord.publish(draft)

    return record
