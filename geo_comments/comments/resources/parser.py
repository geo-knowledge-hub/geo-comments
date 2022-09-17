# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resource Parser."""

from flask_resources import from_conf, request_body_parser, request_parser

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

request_comment_view_args = request_parser(
    from_conf("request_comment_view_args"), location="view_args"
)

#
# Headers
#
request_headers = request_parser(from_conf("request_headers"), location="headers")
