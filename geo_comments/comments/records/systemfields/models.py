# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment entity abstraction fields."""

from invenio_accounts.models import User as InvenioUser
from invenio_records.dictutils import dict_lookup


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


class BaseRecordEntity(EntityBase):
    """Base Record entity abstraction class."""

    entity_cls = None
    """Record entity class."""

    @classmethod
    def from_object(cls, instance):
        """Create a Record entity from an object."""
        if type(instance) == dict:
            record_identifier = dict_lookup(instance, "record_pid")
            obj = cls.entity_cls.pid.resolve(record_identifier)

        else:
            # note: assuming the instance model class
            # (in this case `FeedbackRecord`).
            record_identifier = getattr(instance.model, "record_id")
            obj = cls.entity_cls.get_record(record_identifier)

        return (
            cls(
                entity=obj,
            )
            if record_identifier
            else None
        )

    def dump(self):
        """Dump the user entity as a dict."""
        return {"record_pid": self._entity.pid.pid_value}


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
