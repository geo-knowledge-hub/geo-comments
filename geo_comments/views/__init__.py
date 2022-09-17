# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Comments views."""

from flask import Blueprint

blueprint = Blueprint("geo_comments_ext", __name__)


@blueprint.record_once
def init(state):
    """Initialize application."""
    app = state.app
    ext = app.extensions["geo-comments"]

    # Register services - cannot be done in extension because
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(ext.package_comment_service, service_id="package_comment")
    sregistry.register(ext.package_feedback_service, service_id="package_feedback")
    sregistry.register(ext.resource_comment_service, service_id="resource_comment")
    sregistry.register(ext.resource_feedback_service, service_id="resource_feedback")

    # Register indexers
    iregistry = app.extensions["invenio-indexer"].registry
    iregistry.register(
        ext.package_comment_service.indexer, indexer_id="package_comment"
    )
    iregistry.register(
        ext.package_feedback_service.indexer, indexer_id="package_feedback"
    )
    iregistry.register(
        ext.resource_comment_service.indexer, indexer_id="resource_comment"
    )
    iregistry.register(
        ext.resource_feedback_service.indexer, indexer_id="resource_feedback"
    )
