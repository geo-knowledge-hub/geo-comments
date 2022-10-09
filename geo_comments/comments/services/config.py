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

from . import facets
from .components import CommentData
from .results import RecordItem, RecordList, RecordMetricItem
from .security.permission import CommentPermissionPolicy


class CommentSearchOptions(SearchOptions):
    """Search Options."""

    facets = {"status": facets.status}


class CommentServiceConfig(RecordServiceConfig):
    """Comment Service configuration."""

    schema = None
    schema_metrics = None

    #
    # Common configurations
    #
    permission_policy_cls = CommentPermissionPolicy

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
    result_metrics_cls = RecordMetricItem

    # Components
    components = [CommentData]
