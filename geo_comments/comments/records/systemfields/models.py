# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment entity abstraction fields."""

from invenio_accounts.models import User as InvenioUser
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_records.dictutils import dict_lookup

from geo_rdm_records.modules.resources.records.api import GEORecord
from geo_rdm_records.modules.packages.records.api import GEOPackageRecord


class EntityBase:
    """Base entity abstraction class."""

    def __init__(self, entity=None):
        """Initializer.

        Args:
            entity (object): Entity object.
        """
        self._entity = entity

    @classmethod
    def from_object(cls, instance):
        """Create a new Entity object from a record instance object.

        Note:
            This method must be overwritten by subclasses.
        """
        pass

    def dump(self):
        """Dump the entity object into a dict.

        Note:
            This method must be overwritten by subclasses.
        """
        pass

    def resolve(self):
        """Resolve the entity object."""
        return self._entity


class UserEntity(EntityBase):
    """User entity abstraction class."""

    entity_cls = InvenioUser

    @classmethod
    def from_object(cls, instance):
        """Create a user entity from an object."""
        if type(instance) == dict:
            user_id = dict_lookup(instance, "user_id")

        else:
            # note: assuming the instance model class
            # (in this case `FeedbackRecord`).
            user_id = getattr(instance.model, "user_id")

        return (
            cls(
                entity=InvenioUser.query.get(user_id),
            )
            if user_id
            else None
        )

    def dump(self):
        """Dump the user entity as a dict."""
        return {"user_id": self._entity.id}


class RecordEntity(EntityBase):
    """Record entity abstraction class."""

    entity_classes = [GEORecord, GEOPackageRecord]

    @classmethod
    def _resolve(cls, pid, op):
        """Resolve object by id."""
        # initial solution: enabling multi classes to be used.
        # Is assumed that, every class on ``entity_classes``
        # list is a ``Record`` instance with PID Data Descriptor.
        for entity_class in cls.entity_classes:
            try:
                if op == "resolve":
                    return entity_class.pid.resolve(pid, registered_only=True)

                elif op == "read":
                    return entity_class.get_record(pid)
            except PIDDoesNotExistError:
                pass
            raise PIDDoesNotExistError(pid_type="recid", pid_value=pid)

    @classmethod
    def from_object(cls, instance):
        """Create a Record entity from an object."""
        if type(instance) == dict:
            record_pid = dict_lookup(instance, "record_pid")
            obj = cls._resolve(record_pid, "resolve")

        else:
            # note: assuming the instance model class
            # (in this case `FeedbackRecord`).
            record_id = getattr(instance.model, "record_id")
            obj = cls._resolve(record_id, "read")

        return (
            cls(
                entity=obj,
            )
            if record_id
            else None
        )

    def dump(self):
        """Dump the user entity as a dict."""
        return {"record_pid": self._entity.pid.pid_value}
