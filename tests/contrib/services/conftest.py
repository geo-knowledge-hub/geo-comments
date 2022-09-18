# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Contrib module test."""

import pytest
from invenio_app.factory import create_api
from invenio_records_resources.proxies import current_service_registry


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return create_api


@pytest.fixture(scope="module")
def service_registry():
    """Service ."""
    return current_service_registry
