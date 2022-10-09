# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service links."""

from invenio_records_resources.services.base.links import LinksTemplate
from invenio_records_resources.services.records.links import Link


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


class CommentLink(Link):
    """Shortcut for writing comment links."""

    @staticmethod
    def vars(record, vars):
        """Variables for the URI template."""
        vars.update({"comment_id": record.id, "pid_value": record.get("record")})


class CommentMetricsLink(Link):
    """Shortcut for writing comment metrics links."""

    @staticmethod
    def vars(record, vars):
        """Variables for the URI template."""
        vars.update({"pid_value": record.get("id")})
