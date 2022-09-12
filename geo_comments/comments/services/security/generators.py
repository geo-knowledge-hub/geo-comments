# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Permission policy generators for the Comment Services."""

import operator
from functools import reduce

from elasticsearch_dsl.query import Q
from flask_principal import UserNeed
from geo_config.security.generators import GeoSecretariat as GeoSecretariatBaseGenerator
from geo_config.security.generators import IfIsEqual
from invenio_access.permissions import authenticated_user
from invenio_records_permissions.generators import Generator


class IfDenied(IfIsEqual):
    """Conditional Generator specialized to define permissions for denied feedbacks."""

    def __init__(self, then_, else_):
        """Initializer."""
        super().__init__(
            field="status",
            equal_to="D",
            then_=then_,
            else_=else_,
        )

    def make_query(self, generators, **kwargs):
        """Make a query for one set of generators.

        Note:
            This code is adapted from: https://github.com/inveniosoftware/invenio-rdm-records/blob/cc6ca4ea5283a888278e4d490b8ee5ca78e912ad/invenio_rdm_records/services/generators.py#L69
        """
        queries = [g.query_filter(**kwargs) for g in generators]
        queries = [q for q in queries if q]
        return reduce(operator.or_, queries) if queries else None

    def query_filter(self, **kwargs):
        """Filters for allowed or denied records."""
        q_denied = Q("match", **{"status": "D"})
        q_allowed = Q("match", **{"status": "A"})

        then_query = self.make_query(self.then_, **kwargs)
        else_query = self.make_query(self.else_, **kwargs)

        return (q_denied & then_query) | (q_allowed & else_query)


class GeoSecretariat(GeoSecretariatBaseGenerator):
    """GEO Secretariat generator."""

    def query_filter(self, identity=None, **kwargs):
        """Filters for current identity as super user."""
        return Q("match", **{"status": "D"}) | Q("match", **{"status": "A"})


class CommentOwner(Generator):
    """Comment Owner generator."""

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        if not record:
            return [authenticated_user]
        return [UserNeed(record.get("user_id"))]

    def query_filter(self, identity=None, **kwargs):
        """Filters for current identity as super user."""
        return Q("term", **{"user_id": identity.id})
