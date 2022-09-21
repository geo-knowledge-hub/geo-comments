# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resolver registry for GEO Comments module."""

from flask import current_app
from invenio_records_resources.references.registry import ResolverRegistryBase


class ResolverRegistry(ResolverRegistryBase):
    """Namespace for resolver functions."""

    @classmethod
    def get_registered_resolvers(cls):
        """Get all currently registered resolvers."""
        return current_app.config["GEO_COMMENTS_ENTITY_RESOLVERS"]
