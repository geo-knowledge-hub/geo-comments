# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Comments views."""

from flask import Blueprint

blueprint = Blueprint("geo_comments_ext", __name__, template_folder="../templates")


@blueprint.record_once
def init(state):
    """Initialize application."""
    app = state.app
    ext = app.extensions["geo-comments"]

    # Register services - cannot be done in extension because
    sregistry = app.extensions["invenio-records-resources"].registry
    # Packages
    sregistry.register(ext.package_comment_service, service_id="package_comment")
    sregistry.register(ext.package_feedback_service, service_id="package_feedback")
    # Resources
    sregistry.register(ext.resource_comment_service, service_id="resource_comment")
    sregistry.register(ext.resource_feedback_service, service_id="resource_feedback")
    # Marketplace
    sregistry.register(
        ext.marketplace_item_comment_service, service_id="marketplace_item_comment"
    )
    sregistry.register(
        ext.marketplace_item_feedback_service, service_id="marketplace_item_feedback"
    )

    # Register indexers
    iregistry = app.extensions["invenio-indexer"].registry
    # Packages
    iregistry.register(
        ext.package_comment_service.indexer, indexer_id="package_comment"
    )
    iregistry.register(
        ext.package_feedback_service.indexer, indexer_id="package_feedback"
    )
    # Resources
    iregistry.register(
        ext.resource_comment_service.indexer, indexer_id="resource_comment"
    )
    iregistry.register(
        ext.resource_feedback_service.indexer, indexer_id="resource_feedback"
    )
    # Marketplace
    iregistry.register(
        ext.marketplace_item_comment_service.indexer,
        indexer_id="marketplace_item_comment",
    )
    iregistry.register(
        ext.marketplace_item_feedback_service.indexer,
        indexer_id="marketplace_item_feedback",
    )
