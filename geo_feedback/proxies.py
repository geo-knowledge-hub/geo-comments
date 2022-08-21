# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Proxy definitions."""

from flask import current_app
from werkzeug.local import LocalProxy

current_feedback = LocalProxy(lambda: current_app.extensions["geo-feedback"])
"""Proxy to the extension."""
