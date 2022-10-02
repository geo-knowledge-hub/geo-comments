# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comments module configuration."""

from invenio_users_resources.resolvers import UserResolver

GEO_COMMENTS_AUTO_APPROVE = False
"""Enable automatic comment approval"""

GEO_COMMENTS_ENTITY_RESOLVERS = [UserResolver()]
