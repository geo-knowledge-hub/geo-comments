# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Contrib module test."""

import pytest
from flask_principal import Identity, RoleNeed, UserNeed
from geo_rdm_records.customizations.records.api import GEORecord
from geo_rdm_records.modules.packages.records.api import GEOPackageRecord
from geo_rdm_records.proxies import current_geo_packages_service
from invenio_access.permissions import any_user, authenticated_user
from invenio_app.factory import create_api
from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_records_resources.proxies import current_service_registry


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return create_api


@pytest.fixture(scope="module")
def authenticated_identity(users):
    """Authenticated identity fixture."""
    user_id = users[0].id

    identity = Identity(user_id)
    identity.provides.add(UserNeed(user_id))
    identity.provides.add(authenticated_user)
    return identity


@pytest.fixture(scope="module")
def superuser_identity(users):
    """Authenticated identity fixture."""
    user_id = users[1].id

    identity = Identity(user_id)
    identity.provides.add(UserNeed(user_id))
    identity.provides.add(RoleNeed("superuser-access"))
    return identity


@pytest.fixture(scope="module")
def anyuser_identity():
    """System identity."""
    identity = Identity(3)
    identity.provides.add(any_user)
    return identity


@pytest.fixture(scope="module")
def another_authenticated_identity():
    """System identity."""
    identity = Identity(4)
    identity.provides.add(UserNeed(4))
    identity.provides.add(authenticated_user)
    return identity


@pytest.fixture(scope="module")
def service_registry():
    """Service ."""
    return current_service_registry


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
