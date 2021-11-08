# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

from flask import Flask

from geo_feedback import GEOFeedback


def test_version():
    """Test version import."""
    from geo_feedback import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = GEOFeedback(app)
    assert 'geo-feedback' in app.extensions

    app = Flask('testapp')
    ext = GEOFeedback()
    assert 'geo-feedback' not in app.extensions
    ext.init_app(app)
    assert 'geo-feedback' in app.extensions


def test_view(base_client):
    """Test view."""
    res = base_client.get("/")
    assert res.status_code == 200
    assert 'Welcome to geo-feedback' in str(res.data)
