# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Contrib module test."""

import pytest
from flask_security import login_user
from invenio_accounts.testutils import login_user_via_session
from invenio_app.factory import create_api


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return create_api


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
