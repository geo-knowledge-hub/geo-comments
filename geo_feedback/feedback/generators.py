# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from flask_principal import ActionNeed, UserNeed

from invenio_access.permissions import authenticated_user
from invenio_records_permissions.generators import Generator


class GeoSecretariat(Generator):
    def needs(self, record=None, **kwargs):
        """Enabling Needs."""

        return [ActionNeed("geo-secretariat-access")]


class FeedbackOwner(Generator):
    def needs(self, record=None, **kwargs):
        if not record:
            return [authenticated_user]

        return [
            UserNeed(record.user_id)
        ]


__all__ = (
    "GeoSecretariat"
)
