# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#


from marshmallow import Schema, fields


class FeedbackCategorySchema(Schema):
    name = fields.String(required=True)
    rating = fields.Float(required=True)


class FeedbackAuthorField(fields.Field):
    email = fields.String(required=True)
    fullname = fields.String(required=True)


class FeedbackSchema(Schema):
    id = fields.Integer(dump_only=True)

    comment = fields.String(required=True)
    categories = fields.List(cls_or_instance=fields.Nested(FeedbackCategorySchema()), required=True)

    author = FeedbackAuthorField(dump_only=True)


__all__ = (
    "FeedbackSchema",
    "FeedbackAuthorField",
    "FeedbackCategorySchema"
)
