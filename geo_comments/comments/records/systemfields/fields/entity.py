# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""System Field entity."""

from invenio_records.systemfields import SystemField


class EntityField(SystemField):
    """System field for managing feedback related entities.

    Note:
        This class is based on the ``invenio-rdm-records``. In specific, its used
        as reference the ``ParentRecordAccess`` class and the related features.

    See:
        Reference class: https://github.com/inveniosoftware/invenio-rdm-records/blob/f3877c2b1482e3c951dc0a261f6cb8ea14a1cb16/invenio_rdm_records/records/systemfields/access/field/parent.py#L143
    """

    def __init__(self, key, entity_obj_class):
        """Initializer.

        Args:
            key (str): Key where the data will be stored in the document.

            entity_obj_class (Type): Entity object class (e.g., User, RDMRecord and so on).
        """
        self._entity_obj_class = entity_obj_class
        super().__init__(key=key)

    def pre_commit(self, instance):
        """Dump the configured values before the record is commited."""
        obj = self.obj(instance)
        if obj is not None:
            instance.update(obj.dump())

    def obj(self, instance):
        """Entity object."""
        obj = self._get_cache(instance)
        if obj is None:
            obj = self._entity_obj_class.from_object(instance)

            if not obj:
                raise ValueError("Object defined is not valid!")

            self._set_cache(instance, obj)
        return obj

    def __get__(self, instance, owner=None):
        """Get the entity object."""
        if instance is None:
            # access by class
            return self

        # access by object
        return self.obj(instance).resolve()

    def __set__(self, instance, value):
        """Set the records access object."""
        setattr(instance.model, self.key, value)
