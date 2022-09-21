# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment services results."""

from invenio_records.dictutils import dict_lookup, dict_merge, dict_set
from invenio_records_resources.services.records.results import ExpandableField
from invenio_records_resources.services.records.results import (
    FieldsResolver as BaseFieldsResolver,
)
from invenio_records_resources.services.records.results import (
    RecordItem as BaseRecordItem,
)
from invenio_records_resources.services.records.results import (
    RecordList as BaseRecordList,
)

from geo_comments.resolvers.registry import ResolverRegistry


class FieldsResolver(BaseFieldsResolver):
    """Resolver the reference record for each of the configured field."""

    def _get_value(self, hit, field):
        """Get field value."""
        value = dict_lookup(hit, field.field_name)

        return {field.field_name: value}  # geo-comments don't use 'nested' definitions

    def _collect_values(self, hits):
        """Collect all field values to be expanded."""
        grouped_values = dict()
        for hit in hits:
            for field in self._fields:
                try:
                    value = self._get_value(hit, field)
                except KeyError:
                    continue
                else:
                    # value is not None
                    v, service = field.get_value_service(value)
                    field.add_service_value(service, v)
                    # collect values (ids) and group by service e.g.:
                    # service_1: (13, 4),
                    # service_2: (uuid1, uuid2, ...)
                    grouped_values.setdefault(service, set())
                    grouped_values[service].add(v)

        return grouped_values

    def expand(self, hit):
        """Return the expanded fields for the given hit."""
        results = dict()
        for field in self._fields:
            try:
                value = self._get_value(hit, field)
            except KeyError:
                continue
            else:
                # value is not None
                v, service = field.get_value_service(value)
                resolved_rec = field.get_dereferenced_record(service, v)
                if not resolved_rec:
                    continue
                output = field.pick(resolved_rec)

                # transform field name (potentially dotted) to nested dicts
                # to keep the nested structure of the field
                d = dict()
                dict_set(d, field.field_name, output)
                # merge dict with previous results
                dict_merge(results, d)

        return results


class RecordItem(BaseRecordItem):
    """Single record result."""

    def __init__(
        self,
        service,
        identity,
        record,
        errors=None,
        links_tpl=None,
        schema=None,
        expandable_fields=None,
        expand=False,
    ):
        """Initializer."""
        super(RecordItem, self).__init__(
            service,
            identity,
            record,
            errors=errors,
            links_tpl=links_tpl,
            schema=schema,
            expandable_fields=expandable_fields,
            expand=expand,
        )

        self._fields_resolver = FieldsResolver(expandable_fields)


class RecordList(BaseRecordList):
    """List of records result."""

    def __init__(
        self,
        service,
        identity,
        results,
        params=None,
        links_tpl=None,
        links_item_tpl=None,
        schema=None,
        expandable_fields=None,
        expand=False,
    ):
        """Initializer."""
        super(RecordList, self).__init__(
            service,
            identity,
            results,
            params=params,
            links_tpl=links_tpl,
            links_item_tpl=links_item_tpl,
            schema=schema,
            expandable_fields=expandable_fields,
            expand=expand,
        )

        self._fields_resolver = FieldsResolver(expandable_fields)


class EntityResolverExpandableField(ExpandableField):
    """Expandable entity resolver field.

    This class uses the Entity resolver registry to retrieve the service
    to get records and the fields to return when serializing the referenced
    record.

    Note:
        This class was adapted from `Invenio Requests`.
    """

    entity_proxy = None

    def get_value_service(self, value):
        """Return the value and the service via entity resolvers."""
        self.entity_proxy = ResolverRegistry.resolve_entity_proxy(value)
        v = self.entity_proxy._parse_ref_dict_id()
        _resolver = self.entity_proxy.get_resolver()
        service = _resolver.get_service()
        return v, service

    def pick(self, resolved_rec):
        """Pick fields defined in the entity resolvers."""
        return self.entity_proxy.pick_resolved_fields(resolved_rec)
