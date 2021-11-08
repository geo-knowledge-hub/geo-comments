# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Proxy definitions."""

from flask import current_app
from werkzeug.local import LocalProxy

current_feedback = LocalProxy(
    lambda: current_app.extensions["geo-feedback"])
"""Proxy to the extension."""
