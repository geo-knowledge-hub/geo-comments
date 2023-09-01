..
    This file is part of GEO Knowledge Hub User's Feedback Component.
    Copyright 2021 GEO Secretariat.

    GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Changes
=======

Version 0.5.0 (2023-09-01)

- Updated ``GEO RDM Records`` to version `0.7.0 <https://github.com/geo-knowledge-hub/geo-rdm-records/blob/master/CHANGES.rst#version-070-2023-09-01>`_.

Version 0.4.1 (2023-05-28)
--------------------------

- Added new e-mail notification template.

Version 0.4.0 (2023-05-01)
--------------------------

- Added ``type`` field to the comments mapping.

Version 0.3.0 (2023-03-02)
--------------------------

- Added mappings compatibility with OpenSearch;
- Fixed Resolver interface compatibility with Invenio Records Resources.

Version 0.2.0 (2023-01-05)
--------------------------

- Initial public release;
- Introduced comments APIs

  - Feedback API: Specialized API to enable users to create feedback about packages and resources;
  - Comments API: Specialized API to enable users to share knowledge using comments.

- Added factory system to enable extensions of the comments API;
- Initial support for email notification (for Feedback and Comments activities);
- Introduced interfaces for the Record Landing page based on `GEO Comments React <https://github.com/geo-knowledge-hub/geo-comments-react>`_.
