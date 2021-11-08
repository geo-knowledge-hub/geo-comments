# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Feedback module for Geo Knowledge Hub"""


def create_feedback_api_blueprint(app):
    """Create Geo Knowledge Hub API blueprint."""
    ext = app.extensions["geo-feedback"]

    return ext.feedback_resource.as_blueprint()


__all__ = (
    "create_feedback_api_blueprint"
)
