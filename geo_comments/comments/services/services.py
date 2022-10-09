# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment service."""

from elasticsearch_dsl import Q
from invenio_records_resources.services import LinksTemplate
from invenio_records_resources.services.records import (
    RecordService as InvenioBaseService,
)
from invenio_records_resources.services.records.schema import ServiceSchemaWrapper
from invenio_records_resources.services.uow import (
    RecordCommitOp,
    RecordDeleteOp,
    unit_of_work,
)

from geo_comments.comments.records.api import CommentStatus

from .links import ActionLinksTemplate
from .metrics import RecordFeedbackMetrics
from .results import EntityResolverExpandableField


class CommentService(InvenioBaseService):
    """Comment service class."""

    #
    # Properties
    #
    @property
    def links_item_tpl(self):
        """Item links template."""
        return ActionLinksTemplate(self.config.links_item, self.config.links_action)

    @property
    def record_associated_cls(self):
        """Class of a record associated to a comment."""
        return self.config.record_associated_cls

    @property
    def expandable_fields(self):
        """Get expandable fields."""
        return [EntityResolverExpandableField("user")]

    #
    # Internal methods
    #
    def _get_associated_record(self, record_id):
        """Get associated request."""
        return self.record_associated_cls.pid.resolve(record_id)

    def _get_comment(self, comment_id, with_deleted=True):
        """Get associated event_id."""
        return self.record_cls.get_record(comment_id, with_deleted=with_deleted)

    @unit_of_work()
    def _change_comment_status(
        self, identity, comment_id, status, expand=False, uow=None
    ):
        """Comment status handler."""
        # searching
        comment = self.record_cls.get_record(id_=comment_id, with_denied=True)

        self.require_permission(identity, "view_associated_record", comment=comment)
        self.require_permission(identity, "change_state", comment=comment)

        # running the components
        self.run_components(
            "change_comment_state",
            identity,
            data=status,
            comment=comment,
            uow=uow,
        )

        uow.register(RecordCommitOp(comment, self.indexer))

        return self.result_item(
            self,
            identity,
            comment,
            links_tpl=self.links_item_tpl,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )

    @unit_of_work()
    def _create(
        self,
        record_cls,
        identity,
        associated_record,
        data,
        auto_approve=False,
        raise_errors=True,
        expand=False,
        uow=None,
    ):
        """Create a comment record."""
        # Permissions
        self.require_permission(
            identity, "view_associated_record", record=associated_record
        )

        # checking schema
        data, errors = self.schema.load(
            data, context={"identity": identity}, raise_errors=raise_errors
        )

        # creating an empty comment
        comment = record_cls.create({})

        # running the components
        self.run_components(
            "create",
            identity,
            data=data,
            comment=comment,
            auto_approve=auto_approve,
            associated_record=associated_record,
            errors=errors,
            uow=uow,
        )

        # Persist record (DB and index)
        uow.register(RecordCommitOp(comment, self.indexer))

        return self.result_item(
            self,
            identity,
            comment,
            links_tpl=self.links_item_tpl,
            errors=errors,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )

    #
    # High-level API.
    #
    @unit_of_work()
    def create(
        self,
        identity,
        associated_record_id,
        data,
        auto_approve=False,
        expand=False,
        uow=None,
    ):
        """Create a comment record."""
        associated_record = self._get_associated_record(associated_record_id)

        return self._create(
            self.record_cls,
            identity,
            associated_record,
            data,
            auto_approve=auto_approve,
            uow=uow,
            expand=expand,
        )

    def read(self, identity, comment_id, expand=False):
        """Read a comment matching the id."""
        # reading the comment
        comment = self.record_cls.get_record(id_=comment_id, with_denied=True)

        # Permissions
        self.require_permission(identity, "view_associated_record", comment=comment)
        self.require_permission(identity, "read", comment=comment)

        return self.result_item(
            self,
            identity,
            comment,
            links_tpl=self.links_item_tpl,
            expand=expand,
        )

    @unit_of_work()
    def update(self, comment_id, identity, data, expand=False, uow=None):
        """Replace a record."""
        comment = self.record_cls.get_record(id_=comment_id)

        # Permissions
        self.require_permission(identity, "view_associated_record", comment=comment)
        self.require_permission(identity, "update", comment=comment)

        data, _ = self.schema.load(
            data,
            context={"identity": identity},
        )

        # Run components
        self.run_components(
            "update",
            identity,
            data=data,
            comment=comment,
            uow=uow,
        )

        uow.register(RecordCommitOp(comment, self.indexer))

        return self.result_item(
            self,
            identity,
            comment,
            links_tpl=self.links_item_tpl,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )

    @unit_of_work()
    def delete(self, comment_id, identity, uow=None):
        """Delete a comment from database and search indexes."""
        comment = self.record_cls.get_record(id_=comment_id)

        # Permissions
        self.require_permission(identity, "view_associated_record", comment=comment)
        self.require_permission(identity, "delete", comment=comment)

        # Run components
        self.run_components(
            "delete",
            identity,
            comment=comment,
            uow=uow,
        )

        uow.register(
            RecordDeleteOp(comment, self.indexer, index_refresh=True, force=True)
        )

        return True

    def search(
        self, identity, associated_record_id, params=None, es_preference=None, **kwargs
    ):
        """Search for records matching the querystring."""
        params = params or {}
        expand = kwargs.pop("expand", False)

        # Permissions
        associated_record = self._get_associated_record(associated_record_id)
        self.require_permission(
            identity, "view_associated_record", record=associated_record
        )

        # Prepare and execute the search
        search = self._search(
            "search",
            identity,
            params,
            es_preference,
            extra_filter=Q("term", record=str(associated_record_id)),
            **kwargs
        )
        search_result = search.execute()

        return self.result_list(
            self,
            identity,
            search_result,
            params,
            links_tpl=LinksTemplate(
                self.config.links_search,
                context={"args": params, "pid_value": associated_record_id},
            ),
            links_item_tpl=self.links_item_tpl,
            expandable_fields=self.expandable_fields,
            expand=expand,
        )

    @unit_of_work()
    def allow_comment(self, identity, comment_id, expand=False, uow=None):
        """Allow comment."""
        return self._change_comment_status(
            identity, comment_id, CommentStatus.ALLOWED, expand=expand, uow=uow
        )

    @unit_of_work()
    def deny_comment(self, identity, comment_id, expand=False, uow=None):
        """Deny comment."""
        return self._change_comment_status(
            identity, comment_id, CommentStatus.DENIED, expand=expand, uow=uow
        )


class FeedbackService(CommentService):
    """Specialized service for feedback management."""

    #
    # Properties
    #
    @property
    def schema_metrics(self):
        """Returns the data schema instance."""
        return ServiceSchemaWrapper(self, schema=self.config.schema_metrics)

    #
    # Auxiliary methods
    #
    def result_metrics(self, *args, **kwargs):
        """Create a metric operation result."""
        return self.config.result_metrics_cls(*args, **kwargs)

    #
    # High-level API.
    #
    def metrics(
        self,
        identity,
        associated_record_id,
        record_cls=None,
        search_opts=None,
        permission_action="read",
        es_preference=None,
    ):
        """Generate feedback metrics from a record."""
        # Permissions
        associated_record = self._get_associated_record(associated_record_id)
        self.require_permission(
            identity, "view_associated_record", record=associated_record
        )

        search = self.create_search(
            identity,
            record_cls or self.record_cls,
            search_opts or self.config.search,
            permission_action=permission_action,
            preference=es_preference,
            extra_filter=Q("term", **{"record": associated_record_id}),
        )

        # Generating metrics
        feedback_metrics = RecordFeedbackMetrics(search).generate()

        return self.result_metrics(
            self,
            identity,
            associated_record,
            feedback_metrics,
            links_tpl=LinksTemplate(
                self.config.links_item_metrics,
            ),
        )
