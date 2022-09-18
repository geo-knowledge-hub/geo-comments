# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test contrib records."""

import pytest
from invenio_db import db
from pytest_lazyfixture import lazy_fixture
from sqlalchemy.exc import NoResultFound

from geo_comments.comments.records.api import CommentStatus
from geo_comments.contrib.packages.comments.api import PackageComment
from geo_comments.contrib.packages.feedbacks.api import PackageFeedback
from geo_comments.contrib.resources.comments.api import ResourceComment
from geo_comments.contrib.resources.feedbacks.api import ResourceFeedback


@pytest.mark.parametrize(
    "record,comment_content,comment_cls",
    [
        (
            lazy_fixture("record_package_simple"),
            lazy_fixture("comment_record_data"),
            PackageComment,
        ),
        (
            lazy_fixture("record_package_simple"),
            lazy_fixture("feedback_record_data"),
            PackageFeedback,
        ),
        (
            lazy_fixture("record_resource_simple"),
            lazy_fixture("comment_record_data"),
            ResourceComment,
        ),
        (
            lazy_fixture("record_resource_simple"),
            lazy_fixture("feedback_record_data"),
            ResourceFeedback,
        ),
    ],
)
def test_api_basic_commenting_workflow(users, record, comment_content, comment_cls):
    """Test basic commenting workflow (Using API)."""
    # 1. Creating a comment
    comment = comment_cls.create(comment_content)

    comment.record = record.id
    comment.user = users[0].id  # normal user

    comment.commit()
    db.session.commit()
    comment_cls.index.refresh()

    # 2. Reading a comment
    # 2.1. Trying to read a denied comment (by default, a comment is denied and must be accepted)
    with pytest.raises(NoResultFound):
        comment_cls.get_record(id_=comment.id)

    # 2.2. Trying to read a denied comment with the correct parameters (`with_denied`)
    package_comment_loaded = comment_cls.get_record(id_=comment.id, with_denied=True)

    # 2.2.1. Checking if the loaded comment is correct
    assert comment.status == CommentStatus.DENIED.value
    assert comment.user == package_comment_loaded.user
    assert comment.record == package_comment_loaded.record
    assert comment.dumps() == package_comment_loaded.dumps()

    # 3. Updating a comment
    # 3.1. Allowing the created comment
    package_comment_loaded.status = CommentStatus.ALLOWED.value

    package_comment_loaded.commit()
    db.session.commit()
    comment_cls.index.refresh()

    # 3.1.1. Checking if the comment was updated correctly
    package_comment_updated = comment_cls.get_record(id_=comment.id)

    assert package_comment_updated.status == CommentStatus.ALLOWED.value
