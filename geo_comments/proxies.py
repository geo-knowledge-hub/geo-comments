# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Proxy definitions."""

from flask import current_app
from werkzeug.local import LocalProxy

current_comments = LocalProxy(lambda: current_app.extensions["geo-comments"])
"""Proxy to the current GEO Comments extension."""
