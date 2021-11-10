# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from flask_resources import request_body_parser, from_conf, request_parser

request_data = request_body_parser(
    parsers=from_conf("request_body_parsers"),
    default_content_type=from_conf("default_content_type")
)

request_view_args = request_parser(
    from_conf("request_view_args"), location="view_args"
)

request_search_args = request_parser(
    from_conf("request_search_args"), location="args"
)

__all__ = (
    "request_data",
    "request_view_args",
    "request_search_args"
)
