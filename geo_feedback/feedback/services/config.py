# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Group on Earth Observations (GEO).
#
# geo-feedback is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from ..schema import FeedbackSchema
from ..records.api import FeedbackRecord
from .components import UserFeedbackMetadata

from ..permission import RecordRatingPermissionPolicy

from invenio_rdm_records.records import RDMRecord


class FeedbackServiceConfig:
    schema = FeedbackSchema

    record_cls = RDMRecord
    feedback_cls = FeedbackRecord

    permission_policy_cls = RecordRatingPermissionPolicy

    # Service components
    components = [
        # position matters
        UserFeedbackMetadata
    ]


__all__ = (
    "FeedbackServiceConfig"
)
