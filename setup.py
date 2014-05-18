# -*- coding: utf-8 -*-
"""
dj-config-url
~~~~~~~~~~~~~

.. image:: https://secure.travis-ci.org/julianwachholz/dj-config-url.png?branch=master

This simple Django utility allows you to utilize
`12factor <http://www.12factor.net/backing-services>`_ inspired
environment variables to configure your Django application.


Usage
-----

Configure your database in ``settings.py`` from ``DATABASE_URL``::

    DATABASES = {'default': dj_config_url.config()}

Parse an arbitrary Database URL::

    DATABASES = {'default': dj_config_url.parse('postgres://...')}

Configure your cache backend::

    CACHES = {'default': dj_config_url.parse('memcache://...')}

Supported configurations
------------------------

Databases
^^^^^^^^^

Support currently exists for PostgreSQL, PostGIS, MySQL and SQLite.

SQLite connects to file based databases. The same URL format is used, omitting
the hostname, and using the "file" portion as the filename of the database.
This has the effect of four slashes being present for an absolute file path:
``sqlite:////full/path/to/your/database/file.sqlite``.

Caches
^^^^^^

``dj-config-url`` currently supports the cache backends in the Django core:
Database, dummy, file based, local memory and memcached.


"""

from setuptools import setup

setup(
    name='dj-config-url',
    version='0.1.0',
    url='https://github.com/julianwachholz/dj-config-url',
    license='BSD',
    author='Julian Wachholz',
    author_email='julian@wachholz.ch',
    description='Use configuration URLs in your Django Application.',
    long_description=__doc__,
    py_modules=['dj_config_url', 'dj_database_url'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
