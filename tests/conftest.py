# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""GEO Comments test configuration."""

import pytest
from flask_principal import Identity, RoleNeed, UserNeed
from flask_security import login_user
from flask_security.utils import hash_password
from geo_rdm_records.modules.marketplace.records.api import GEOMarketplaceItem
from geo_rdm_records.modules.packages.records.api import GEOPackageRecord
from geo_rdm_records.modules.rdm.records.api import GEORecord
from geo_rdm_records.proxies import (
    current_geo_packages_service,
    current_marketplace_service,
)
from invenio_access.models import ActionRoles
from invenio_access.permissions import (
    any_user,
    authenticated_user,
    superuser_access,
    system_identity,
)
from invenio_accounts.models import Role
from invenio_accounts.testutils import login_user_via_session
from invenio_app.factory import create_api as _create_api
from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_vocabularies.proxies import current_service as vocabulary_service
from invenio_vocabularies.records.api import Vocabulary


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

        basic_user = datastore.create_user(
            email="basic@example.org", password=hash_password("password"), active=True
        )

        basic_user2 = datastore.create_user(
            email="basic2@example.org", password=hash_password("password"), active=True
        )

        admin_user = datastore.create_user(
            email="admin@example.org", password=hash_password("password"), active=True
        )
        admin_user.roles.append(su_role)

    db.session.commit()
    return [basic_user, basic_user2, admin_user]


#
# Identities
#
@pytest.fixture(scope="module")
def authenticated_identity(users):
    """Authenticated identity fixture."""
    user_id = users[0].id

    identity = Identity(user_id)
    identity.provides.add(any_user)
    identity.provides.add(UserNeed(user_id))
    identity.provides.add(authenticated_user)
    return identity


@pytest.fixture(scope="module")
def superuser_identity(users):
    """Authenticated identity fixture."""
    user_id = users[-1].id

    identity = Identity(user_id)
    identity.provides.add(UserNeed(user_id))
    identity.provides.add(RoleNeed("superuser-access"))
    return identity


@pytest.fixture(scope="module")
def anyuser_identity():
    """System identity."""
    identity = Identity(4)
    identity.provides.add(any_user)
    return identity


@pytest.fixture(scope="module")
def another_authenticated_identity():
    """System identity."""
    identity = Identity(5)
    identity.provides.add(any_user)
    identity.provides.add(UserNeed(5))
    identity.provides.add(authenticated_user)
    return identity


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
    return {"content": "A comment here"}


@pytest.fixture(scope="module")
def feedback_record_data():
    """Data to create a feedback comment."""
    return {
        "content": "A comment here",
        "topics": [
            {"name": "Test A", "rating": 12.4},
            {"name": "Test B", "rating": 15.5},
        ],
    }


#
# Data fixtures
#
@pytest.fixture(scope="module")
def resource_type_type(app):
    """Resource type vocabulary type."""
    return vocabulary_service.create_type(system_identity, "resourcetypes", "rsrct")


@pytest.fixture(scope="module")
def resource_type_v(app, resource_type_type):
    """Resource type vocabulary record."""
    resource_types = [
        {  # create base resource type
            "id": "image",
            "props": {
                "csl": "figure",
                "datacite_general": "Image",
                "datacite_type": "",
                "openaire_resourceType": "25",
                "openaire_type": "dataset",
                "eurepo": "info:eu-repo/semantic/other",
                "schema.org": "https://schema.org/ImageObject",
                "subtype": "",
                "type": "image",
            },
            "icon": "chart bar outline",
            "title": {"en": "Image"},
            "tags": ["depositable", "linkable"],
            "type": "resourcetypes",
        },
        {
            "id": "image-photo",
            "props": {
                "csl": "graphic",
                "datacite_general": "Image",
                "datacite_type": "Photo",
                "openaire_resourceType": "25",
                "openaire_type": "dataset",
                "eurepo": "info:eu-repo/semantic/other",
                "schema.org": "https://schema.org/Photograph",
                "subtype": "image-photo",
                "type": "image",
            },
            "icon": "chart bar outline",
            "title": {"en": "Photo"},
            "tags": ["depositable", "linkable"],
            "type": "resourcetypes",
        },
        {
            "id": "knowledge",
            "props": {
                "csl": "article",
                "datacite_general": "Other",
                "datacite_type": "",
                "openaire_resourceType": "20",
                "openaire_type": "other",
                "eurepo": "info:eu-repo/semantics/other",
                "schema.org": "https://schema.org/CreativeWork",
                "subtype": "",
                "type": "knowledge",
            },
            "icon": "asterisk",
            "title": {"en": "Knowledge Package"},
            "tags": ["depositable", "linkable"],
            "type": "resourcetypes",
        },
    ]

    for resource_type in resource_types:
        vocabulary_service.create(system_identity, resource_type)

    Vocabulary.index.refresh()


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
            "publication_date": "2020-06-01",
            "resource_type": {"id": "image-photo"},
            "creators": [
                {
                    "person_or_org": {
                        "family_name": "Brown",
                        "given_name": "Troy",
                        "type": "personal",
                    }
                }
            ],
            "title": "A Romans story",
        },
    }


@pytest.fixture(scope="module")
def record_resource_simple(
    location, resource_type_v, authenticated_identity, minimal_record
):
    """Basic Resource Record."""
    record_item = current_rdm_records_service.create(
        authenticated_identity, minimal_record
    )
    record_item = current_rdm_records_service.publish(
        authenticated_identity, record_item["id"]
    )

    return GEORecord.pid.resolve(record_item["id"])


@pytest.fixture(scope="module")
def record_package_simple(
    location, resource_type_v, authenticated_identity, minimal_record
):
    """Basic Package Record."""
    record_item = current_geo_packages_service.create(
        authenticated_identity, minimal_record
    )
    record_item = current_geo_packages_service.publish(
        authenticated_identity, record_item["id"]
    )

    return GEOPackageRecord.pid.resolve(record_item["id"])


@pytest.fixture(scope="module")
def record_marketplace_item_simple(
    location, resource_type_v, authenticated_identity, minimal_record
):
    """Basic Package Record."""
    record_item = current_marketplace_service.create(
        authenticated_identity, minimal_record
    )
    record_item = current_marketplace_service.publish(
        authenticated_identity, record_item["id"]
    )

    return GEOMarketplaceItem.pid.resolve(record_item["id"])
