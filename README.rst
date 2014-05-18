DJ-Config-URL
~~~~~~~~~~~~~

.. image:: https://secure.travis-ci.org/julianwachholz/dj-config-url.png?branch=master
   :target: http://travis-ci.org/julianwachholz/dj-config-url

This simple Django utility allows you to utilize
`12factor <http://www.12factor.net/backing-services>`_ inspired
environment variables to configure your Django application.

This project has been forked from kennethreitz' `dj-database-url` and is fully
compatible with it, so you can use this utility as a drop-in replacement.

Supported configuration
-----------------------

Support currently exists for the following database engines: PostgreSQL,
PostGIS, MySQL, MySQL (GIS) and SQLite.

You can also configure your ``CACHES`` configuration for the backends supported
by the Django core: Database, dummy, file based, local memory as well as both
Memcached backends.

Installation
------------

Installation is simple::

    $ pip install dj-config-url

Usage
-----

Configure your database in ``settings.py`` from ``DATABASE_URL``::

    DATABASES = {'default': dj_config_url.config()}

Parse an arbitrary Database URL::

    DATABASES = {'default': dj_config_url.parse('postgres://...')}

Configure your cache backend::

    CACHES = {'default': dj_config_url.parse('memcache://...')}

Use a custom cache backend class::

    CACHES = {'default': dj_config_url.parse('memcache://127.0.0.1:123?password=s3cr3t', 'redis_cache.cache.RedisCache')}


Database examples
^^^^^^^^^^^^^^^^^

===========  ==========================================  ============================================
Engine       Django Backend                              URL
===========  ==========================================  ============================================
PostgreSQL   ``django.db.backends.postgresql_psycopg2``  ``postgres://USER:PASSWORD@HOST:PORT/NAME``
PostGIS      ``django.contrib.gis.db.backends.postgis``  ``postgis://USER:PASSWORD@HOST:PORT/NAME``
MySQL        ``django.db.backends.mysql``                ``mysql://USER:PASSWORD@HOST:PORT/NAME``
MySQL (GIS)  ``django.contrib.gis.db.backends.mysql``    ``mysqlgis://USER:PASSWORD@HOST:PORT/NAME``
SQLite       ``django.db.backends.sqlite3``              ``sqlite:///PATH`` [1]_
===========  ==========================================  ============================================

.. [1] SQLite connects to file based databases. The same URL format is used, omitting
       the hostname, and using the "file" portion as the filename of the database.
       This has the effect of four slashes being present for an absolute file path:
       ``sqlite:////full/path/to/your/database/file.sqlite``.


Cache examples
^^^^^^^^^^^^^^

============  =======================================================  ========================================
Backend       Django Backend                                           URL
============  =======================================================  ========================================
Database      ``django.core.cache.backends.db.DatabaseCache``          ``dbcache://table_name``
Dummy         ``django.core.cache.backends.dummy.DummyCache``          ``dummycache://``
File based    ``django.core.cache.backends.filebased.FileBasedCache``  ``filecache:///path/to/cache``
Local Memory  ``django.core.cache.backends.locmem.LocMemCache``        ``locmemcache://[optional name]``
Memcached     ``django.core.cache.backends.memcached.MemcachedCache``  ``memcache://IP:PORT[,IP:PORT, ...]``
PyLibMC       ``django.core.cache.backends.memcached.PyLibMCCache``    ``pymemcache://IP:PORT[,IP:PORT, ...]``
============  =======================================================  ========================================

You may specify options for the cache backends as query parameters in the url, e.g.::

    CACHES = {
        'default': dj_config_url.parse('filecache:///var/tmp/django_cache?timeout=60&max_entries=1000&cull_frequency=2'),
    }

This will be equivalent of writing this in your ``settings.py``::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
            'TIMEOUT': 60,
            'OPTIONS': {
                'MAX_ENTRIES': 1000,
                'CULL_FREQUENCY': 2,
            }
        }
    }
