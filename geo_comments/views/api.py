# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comments module for Geo Knowledge Hub."""


def create_package_comment_api_blueprint(app):
    """Create the Package comments API Blueprint."""
    ext = app.extensions["geo-comments"]

    return ext.package_comment_resource.as_blueprint()


def create_package_feedback_api_blueprint(app):
    """Create the Package comments API Blueprint."""
    ext = app.extensions["geo-comments"]

    return ext.package_feedback_resource.as_blueprint()


def create_resource_comment_api_blueprint(app):
    """Create the Package's resource comments API Blueprint."""
    ext = app.extensions["geo-comments"]

    return ext.resource_comment_resource.as_blueprint()


def create_resource_feedback_api_blueprint(app):
    """Create the Package's resource feedbacks API Blueprint."""
    ext = app.extensions["geo-comments"]

    return ext.resource_feedback_resource.as_blueprint()


def create_marketplace_item_comment_api_blueprint(app):
    """Create the Package's resource comments API Blueprint."""
    ext = app.extensions["geo-comments"]

    return ext.marketplace_item_comment_resource.as_blueprint()


def create_marketplace_item_feedback_api_blueprint(app):
    """Create the Package's resource feedbacks API Blueprint."""
    ext = app.extensions["geo-comments"]

    return ext.marketplace_item_feedback_resource.as_blueprint()
