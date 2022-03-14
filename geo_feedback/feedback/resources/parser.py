# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from flask_resources import request_body_parser, from_conf, request_parser

#
# Request args
#
request_data = request_body_parser(
    parsers=from_conf("request_body_parsers"),
    default_content_type=from_conf("default_content_type"),
)

#
# Args
#
request_read_args = request_parser(from_conf("request_read_args"), location="args")
request_search_args = request_parser(from_conf("request_search_args"), location="args")

request_feedback_view_args = request_parser(
    from_conf("request_feedback_view_args"), location="view_args"
)

#
# Headers
#
request_headers = request_parser(from_conf("request_headers"), location="headers")
