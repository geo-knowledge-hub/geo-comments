..
    This file is part of GEO Knowledge Hub User's Comments Component.
    Copyright 2021-2022 GEO Secretariat.

    GEO Knowledge Hub User's Comments Component is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

============
GEO Comments
============

.. image:: https://github.com/geo-knowledge-hub/geo-comments/workflows/CI/badge.svg
        :target: https://github.com/geo-knowledge-hub/geo-comments/actions?query=workflow%3ACI
        :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/lifecycle-maturing-blue.svg
        :target: https://www.tidyverse.org/lifecycle/#maturing
        :alt: Software Life Cycle

.. image:: https://img.shields.io/github/license/geo-knowledge-hub/geo-comments.svg
        :target: https://github.com/geo-knowledge-hub/geo-comments/blob/master/LICENSE
        :alt: Software License

.. image:: https://img.shields.io/github/tag/geo-knowledge-hub/geo-comments.svg
        :target: https://github.com/geo-knowledge-hub/geo-comments/releases
        :alt: Release

.. image:: https://img.shields.io/discord/730739436551143514?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/730739436551143514#
        :alt: Join us at Discord

GEO Knowledge Hub comments module.

Development
===========

Install
-------

Install the package with the `docs`, `elasticsearch`, and a `database` (postgresql in the example) dependencies:

.. code-block:: console

    pip install -e .[docs,postgresql,elasticsearch7]


Tests
-----

After installing the package and its dependencies, if you want to test the code, install the `tests` dependencies:

.. code-block:: console

    pip install -e .[tests,elasticsearch7]

Now, you can run the tests:

.. code-block:: console

    ./run-tests.sh
