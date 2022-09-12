# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Contrib - Packages API tests."""

import pytest
from invenio_db import db

from geo_comments.contrib.packages.comments.api import PackageComment


def test_api_basic_comment_workflow(
    users, comment_record_data, feedback_record_data, record_package_simple
):
    """Test Packages API Basic workflow."""
    # Comments

    # 1. Creating a comment
    package_comment = PackageComment.create(comment_record_data)

    package_comment.record = record_package_simple.id
    package_comment.user = users[0].id  # normal user

    # package_comment.commit()
    # db.session.commit()

    # 2. Reading a comment
    # package_comment_loaded = PackageComment.get_record(id_=package_comment.id)
    # db.session.commit()
    # PackageComment.index.refresh()
    #
    # assert package_comment.user == package_comment_loaded.user
    # assert package_comment.record == package_comment_loaded.record
    # assert package_comment.dumps() == package_comment_loaded.dumps()

    # Feedbacks
