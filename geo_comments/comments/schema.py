# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment schemas."""

from marshmallow import Schema, fields, validate
from marshmallow_utils.fields import SanitizedHTML, SanitizedUnicode


#
# Base comment schema
#
class CommentSchema(Schema):
    """Comment schema class."""

    id = fields.UUID(dump_only=True)

    content = SanitizedHTML(required=True)

    status = SanitizedUnicode(
        validate=lambda obj: (validate.OneOf(choices=["A", "D"]))(obj),
        dump_only=True,
        required=True,
    )

    user_id = fields.Integer(required=True, dump_only=True, attribute="user_id")
    record_pid = SanitizedUnicode(
        required=True, dump_only=False, attribute="record_pid"
    )


#
# Specialized comments schema
#

# Feedback
class FeedbackTopicSchema(Schema):
    """Feedback Topic schema class."""

    rating = fields.Number(required=True)
    name = SanitizedUnicode(required=True)


class FeedbackCommentSchema(CommentSchema):
    """Comment schema class."""

    topics = fields.List(
        cls_or_instance=fields.Nested(FeedbackTopicSchema()), required=True
    )
