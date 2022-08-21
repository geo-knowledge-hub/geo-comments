..
    This file is part of GEO Knowledge Hub User's Feedback Component.
    Copyright 2021 GEO Secretariat.

    GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

============
GEO Feedback
============

.. image:: https://github.com/geo-knowledge-hub/geo-feedback/workflows/CI/badge.svg
        :target: https://github.com/geo-knowledge-hub/geo-feedback/actions?query=workflow%3ACI
        :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/lifecycle-maturing-blue.svg
        :target: https://www.tidyverse.org/lifecycle/#maturing
        :alt: Software Life Cycle

.. image:: https://img.shields.io/github/license/geo-knowledge-hub/geo-feedback.svg
        :target: https://github.com/geo-knowledge-hub/geo-feedback/blob/master/LICENSE
        :alt: Software License

.. image:: https://img.shields.io/github/tag/geo-knowledge-hub/geo-feedback.svg
        :target: https://github.com/geo-knowledge-hub/geo-feedback/releases
        :alt: Release

.. image:: https://img.shields.io/discord/730739436551143514?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/730739436551143514#
        :alt: Join us at Discord

GEO Knowledge Hub feedback module.

About
-----

This package contains a component to allow users expressing their experience about a Knowledge Package in the `GEO Knowledge Hub <https://github.com/geo-knowledge-hub/geo-knowledge-hub>`_. Currently there are three major points to be rated by a user:

- **Clarity:** The package and its components contain enough documentation and clear descriptions.

- **Usefulness:** The package helps solving a challenge and makes use of accessible, relevant tools and data.

- **Reusability:** The package and its components are organized and linked in a way that allows the used to fully reuse it.

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
