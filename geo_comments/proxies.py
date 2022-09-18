# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Proxy definitions."""

from flask import current_app
from werkzeug.local import LocalProxy


def _ext_proxy(attr):
    return LocalProxy(lambda: getattr(current_app.extensions["geo-comments"], attr))


current_service = _ext_proxy("service")
"""Proxy to the instantiated comment service."""


current_resource = _ext_proxy("resource")
"""Proxy to the instantiated comment resource."""
