# -*- coding: utf-8 -*-
#
# This file is part of GEO Knowledge Hub User's Feedback Component.
# Copyright 2021 GEO Secretariat.
#
# GEO Knowledge Hub User's Feedback Component is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Feedback module for GEO Knowledge Hub User's Feedback Component."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'pytest-invenio>=1.4.0',
]

invenio_db_version = '>=1.0.9,<2.0.0'
invenio_search_version = '>=1.4.2,<2.0.0'

extras_require = {
    'docs': [
        'Sphinx>=3,<4',
    ],
    'elasticsearch6': [
        f'invenio-search[elasticsearch6]{invenio_search_version}',
    ],
    'elasticsearch7': [
        f'invenio-search[elasticsearch7]{invenio_search_version}',
    ],
    'postgresql': [
        f'invenio-db[postgresql,versioning]{invenio_db_version}',
    ],
    'tests': tests_require,
}

extras_require['all'] = [req for _, reqs in extras_require.items() for req in reqs]

setup_requires = [
    'Babel>=2.8',
]

install_requires = [
    'invenio-i18n>=1.2.0',
    'invenio-rdm-records>=0.32.3,<0.33.0',
    'sqlalchemy-json>=0.4.0'
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('geo_feedback', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='geo-feedback',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='Geo Knowledge Hub',
    license='MIT',
    author='GEO Secretariat',
    author_email='geokhub@geosec.org',
    url='https://github.com/geo-knowledge-hub/geo-feedback',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'geo_feedback = geo_feedback:GEOFeedback',
        ],
        'invenio_db.models': [
            'geo_feedback = geo_feedback.feedback.records.models'
        ],
        'invenio_config.module': [
            "geo_feedback = geo_feedback.config",
        ],
        'invenio_base.api_apps': [
            'geo_feedback = geo_feedback:GEOFeedback',
        ],
        'invenio_assets.webpack': [
            'geo_feedback = geo_feedback.theme.webpack:theme'
        ],
        'invenio_base.api_blueprints': [
            'geo_feedback = geo_feedback.views:create_feedback_api_blueprint',
        ],
        'invenio_i18n.translations': [
            'messages = geo_feedback',
        ],
        # 'invenio_access.actions': [],
        # 'invenio_admin.actions': [],
        # 'invenio_assets.bundles': [],
        # 'invenio_base.blueprints': [],
        # 'invenio_records.jsonresolver': [],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 1 - Planning',
    ],
)
