# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Feedback service config."""

from invenio_rdm_records.records.api import RDMRecord
from invenio_records_resources.services.records.config import (
    RecordServiceConfig,
    SearchOptions,
)
from invenio_records_resources.services.records.links import pagination_links
from invenio_records_resources.services.records.results import RecordItem, RecordList

from geo_comments.comments.records.api import CommentRecord
from geo_comments.comments.schema import CommentSchema
from geo_comments.comments.services import facets
from geo_comments.comments.services.components import FeedbackData
from geo_comments.comments.services.links import FeedbackLink
from geo_comments.comments.services.security.permission import FeedbackPermissionPolicy


class FeedbackSearchOptions(SearchOptions):
    """Search Options for the Feedback."""

    facets = {"status": facets.status, "record": facets.record}


class FeedbackServiceConfig(RecordServiceConfig):
    """Feedback service configuration."""

    schema = CommentSchema

    #
    # Common configurations
    #
    permission_policy_cls = FeedbackPermissionPolicy

    #
    # Search configurations
    #
    search = FeedbackSearchOptions

    #
    # Record API configuration
    #
    record_cls = CommentRecord

    record_associated_cls = RDMRecord

    #
    # Service configuration
    #
    links_item = {"self": FeedbackLink("{+api}/feedbacks?q=id:{id}")}

    links_search = pagination_links("{+api}/feedbacks{?args*}")

    links_action = {
        "allow": FeedbackLink(
            "{+api}/feedbacks/actions/allow?q=id:{id}",
        ),
        "deny": FeedbackLink(
            "{+api}/feedbacks/actions/deny?q=id:{id}",
        ),
    }

    # Results
    result_item_cls = RecordItem
    result_list_cls = RecordList

    # Components
    components = [FeedbackData]
