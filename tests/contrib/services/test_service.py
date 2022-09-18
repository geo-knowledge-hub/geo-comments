# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test contrib services."""

import pytest
from invenio_records_resources.services.errors import PermissionDeniedError
from pytest_lazyfixture import lazy_fixture

from geo_comments.comments.records.api import CommentStatus
from geo_comments.contrib.packages.comments.api import PackageComment
from geo_comments.contrib.packages.feedbacks.api import PackageFeedback
from geo_comments.contrib.resources.comments.api import ResourceComment
from geo_comments.contrib.resources.feedbacks.api import ResourceFeedback


@pytest.mark.parametrize(
    "service_name,comment_cls,record,comment_content",
    [
        (
            "package_comment",
            PackageComment,
            lazy_fixture("record_package_simple"),
            lazy_fixture("comment_record_data"),
        ),
        (
            "package_feedback",
            PackageFeedback,
            lazy_fixture("record_package_simple"),
            lazy_fixture("feedback_record_data"),
        ),
        (
            "resource_comment",
            ResourceComment,
            lazy_fixture("record_resource_simple"),
            lazy_fixture("comment_record_data"),
        ),
        (
            "resource_feedback",
            ResourceFeedback,
            lazy_fixture("record_resource_simple"),
            lazy_fixture("feedback_record_data"),
        ),
    ],
)
def test_service_basic_commenting_workflow(
    authenticated_identity,
    superuser_identity,
    anyuser_identity,
    another_authenticated_identity,
    service_registry,
    service_name,
    comment_cls,
    record,
    comment_content,
):
    """Test basic commenting workflow using service."""
    # 1. Getting the correct service
    service = service_registry.get(service_name)

    # 2. Creating a comment
    comment = service.create(authenticated_identity, record.id, comment_content)

    # 2.1. Checking comment created properties
    assert comment["record_pid"] == record.pid.pid_value
    assert comment["user_id"] == authenticated_identity.id
    assert comment["content"] == comment_content["content"]
    assert comment["status"] == CommentStatus.DENIED.value

    # 3. Reading the comment
    # 3.1. User who created the comment can read it
    comment_id = comment["id"]
    comment_loaded = service.read(authenticated_identity, comment_id)

    assert comment_loaded.to_dict() == comment.to_dict()

    # 3.2. Trying to read the denied comment with an authenticated user
    with pytest.raises(PermissionDeniedError):
        service.read(anyuser_identity, comment_id)

    # 4. Allowing the comment in the system
    # 4.1. Trying using an authenticated user
    with pytest.raises(PermissionDeniedError):
        service.allow_comment(another_authenticated_identity, comment_id)

    # 4.2. Trying using an unauthenticated user
    with pytest.raises(PermissionDeniedError):
        service.allow_comment(anyuser_identity, comment_id)

    # 4.3. Trying using an admin user
    allowed_comment = service.allow_comment(superuser_identity, comment_id)

    assert allowed_comment["status"] == CommentStatus.ALLOWED.value

    comment_cls.index.refresh()

    # 4.4. Checking the comment with changed state
    # 4.4.1. Reading with the owner of the comment
    service.read(authenticated_identity, comment_id)

    # 4.4.2. Reading with an unauthenticated user (ToDo)
    # service.read(anyuser_identity, comment_id)

    # 5. Searching for the comment by record
    search_result = service.search(authenticated_identity)

    assert search_result.total != 0
    assert next(search_result.hits).get('status') == CommentStatus.ALLOWED.value
    assert next(search_result.hits).get('user_id') == authenticated_identity.id
