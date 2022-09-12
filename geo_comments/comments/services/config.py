# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment service config."""

from invenio_records_resources.services.records.config import (
    RecordServiceConfig,
    SearchOptions,
)
from invenio_records_resources.services.records.links import pagination_links
from invenio_records_resources.services.records.results import RecordItem, RecordList

from geo_comments.comments.schema import CommentSchema, FeedbackCommentSchema
from geo_comments.comments.services import facets
from geo_comments.comments.services.components import CommentData
from geo_comments.comments.services.links import CommentLink
from geo_comments.comments.services.security.permission import FeedbackPermissionPolicy


class CommentSearchOptions(SearchOptions):
    """Search Options."""

    facets = {"status": facets.status, "record": facets.record}


class BaseCommentServiceConfig(RecordServiceConfig):
    """Comment Service configuration."""

    schema = None

    #
    # Common configurations
    #
    permission_policy_cls = FeedbackPermissionPolicy

    #
    # Search configurations
    #
    search = CommentSearchOptions

    #
    # Record API configuration
    #
    record_cls = None  # must be overridden

    record_associated_cls = None  # must be overridden

    # Results
    result_item_cls = RecordItem
    result_list_cls = RecordList

    # Components
    components = [CommentData]


class CommentServiceConfig(RecordServiceConfig):
    """Comment Service configuration."""

    service_id = "comment_service"

    schema = CommentSchema

    #
    # Service configuration
    #
    links_item = {"self": CommentLink("{+api}/comments?q=id:{id}")}

    links_search = pagination_links("{+api}/comments{?args*}")

    links_action = {
        "allow": CommentLink(
            "{+api}/comments/actions/allow?q=id:{id}",
        ),
        "deny": CommentLink(
            "{+api}/comments/actions/deny?q=id:{id}",
        ),
    }


class FeedbackServiceConfig(RecordServiceConfig):
    """Feedback Service configuration."""

    service_id = "feedback_service"

    schema = FeedbackCommentSchema

    #
    # Service configuration
    #
    links_item = {"self": CommentLink("{+api}/feedbacks?q=id:{id}")}

    links_search = pagination_links("{+api}/feedbacks{?args*}")

    links_action = {
        "allow": CommentLink(
            "{+api}/feedbacks/actions/allow?q=id:{id}",
        ),
        "deny": CommentLink(
            "{+api}/feedbacks/actions/deny?q=id:{id}",
        ),
    }
