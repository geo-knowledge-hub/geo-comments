# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comments module for Geo Knowledge Hub."""


def create_comments_api_blueprint(app):
    """Create GEO Knowledge Hub API blueprint."""
    ext = app.extensions["geo-comments"]

    return ext.comments_resource.as_blueprint()
