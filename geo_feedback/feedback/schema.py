# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Feedback schema."""

from marshmallow import Schema, fields, validate
from marshmallow_utils.fields import SanitizedHTML, SanitizedUnicode


class FeedbackTopicSchema(Schema):
    """Feedback Topic schema class."""

    rating = fields.Number(required=True)
    name = SanitizedUnicode(required=True)


class FeedbackSchema(Schema):
    """Feedback schema class."""

    id = fields.UUID(dump_only=True)

    comment = SanitizedHTML(required=True)
    topics = fields.List(
        cls_or_instance=fields.Nested(FeedbackTopicSchema()), required=True
    )

    status = SanitizedUnicode(
        validate=lambda obj: (validate.OneOf(choices=["A", "D"]))(obj),
        dump_only=True,
        required=True,
    )

    user_id = fields.Integer(required=True, dump_only=True, attribute="user_id")
    record_pid = SanitizedUnicode(
        required=True, dump_only=False, attribute="record_pid"
    )
