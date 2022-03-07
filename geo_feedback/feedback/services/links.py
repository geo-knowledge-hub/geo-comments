# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from invenio_records_resources.services.records.links import Link

from invenio_records_resources.services.base.links import LinksTemplate


class ActionLinksTemplate(LinksTemplate):
    """Templates for generating links with action objects."""

    def __init__(self, links, links_action, context=None):
        """Initializer."""
        super(ActionLinksTemplate, self).__init__(links, context=context)

        self._links_action = links_action

    def expand(self, obj):
        """Expand all the link templates."""

        links = {"actions": {}}
        ctx = self.context
        for key, link in self._links.items():
            if link.should_render(obj, ctx):
                links[key] = link.expand(obj, ctx)

        # expanding the links actions.
        for action_name, action_link in self._links_action.items():
            if action_link.should_render(obj, ctx):
                links["actions"][action_name] = action_link.expand(obj, ctx)

        return links


class FeedbackLink(Link):
    """Short cut for writing feedback links."""

    @staticmethod
    def vars(record, vars):
        """Variables for the URI template."""
        vars.update({"id": record.id})
