# -*- coding: utf-8 -*-

import os

try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse


# Register database schemes in URLs.
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('postgresql')
urlparse.uses_netloc.append('pgsql')
urlparse.uses_netloc.append('postgis')
urlparse.uses_netloc.append('mysql')
urlparse.uses_netloc.append('mysql2')
urlparse.uses_netloc.append('mysqlgis')
urlparse.uses_netloc.append('spatialite')
urlparse.uses_netloc.append('sqlite')

urlparse.uses_netloc.append('dbcache')
urlparse.uses_netloc.append('dummycache')
urlparse.uses_netloc.append('filecache')
urlparse.uses_netloc.append('locmemcache')
urlparse.uses_netloc.append('memcache')
urlparse.uses_netloc.append('pymemcache')


DEFAULT_DB_ENV = 'DATABASE_URL'
DEFAULT_CACHE_ENV = 'CACHE_URL'

DB_SCHEMES = {
    'postgres': 'django.db.backends.postgresql_psycopg2',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'pgsql': 'django.db.backends.postgresql_psycopg2',
    'postgis': 'django.contrib.gis.db.backends.postgis',
    'mysql': 'django.db.backends.mysql',
    'mysql2': 'django.db.backends.mysql',
    'mysqlgis': 'django.contrib.gis.db.backends.mysql',
    'spatialite': 'django.contrib.gis.db.backends.spatialite',
    'sqlite': 'django.db.backends.sqlite3',
}

_DB_BASE_OPTIONS = ['CONN_MAX_AGE', 'ATOMIC_REQUESTS', 'AUTOCOMMIT']

CACHE_SCHEMES = {
    'dbcache': 'django.core.cache.backends.db.DatabaseCache',
    'dummycache': 'django.core.cache.backends.dummy.DummyCache',
    'filecache': 'django.core.cache.backends.filebased.FileBasedCache',
    'locmemcache': 'django.core.cache.backends.locmem.LocMemCache',
    'memcache': 'django.core.cache.backends.memcached.MemcachedCache',
    'pymemcache': 'django.core.cache.backends.memcached.PyLibMCCache',
}

_CACHE_BASE_OPTIONS = ['TIMEOUT', 'KEY_PREFIX', 'VERSION', 'KEY_FUNCTION']


def config(env=DEFAULT_DB_ENV, default=None, engine=None):
    """Returns config dictionary from the specified environment variable."""

    config = {}

    s = os.environ.get(env, default)

    if s:
        config = parse(s, engine)

    return config


def cache_config(env=DEFAULT_CACHE_ENV, default=None, engine=None):
    """Returns a config dictionary, defaulting to CACHE_URL."""
    return config(env, default, engine)


# return int if possible
_cast_int = lambda v: int(v) if isinstance(v, str) and v.isdigit() else v


def _parse_db(url, engine=None):
    """Parses a database config url."""
    config = {}

    # Remove query strings.
    path = url.path[1:]
    path = path.split('?', 2)[0]

    # if we are using sqlite and we have no path, then assume we
    # want an in-memory database (this is the behaviour of sqlalchemy)
    if url.scheme == 'sqlite' and path == '':
        path = ':memory:'

    # Update with environment configuration.
    config.update({
        'NAME': path or '',
        'USER': url.username or '',
        'PASSWORD': url.password or '',
        'HOST': url.hostname or '',
        'PORT': url.port or '',
    })

    if url.query:
        config_options = {}
        for k, v in urlparse.parse_qs(url.query).items():
            if k.upper() in _DB_BASE_OPTIONS:
                config.update({k.upper(): _cast_int(v[0])})
            else:
                config_options.update({k: _cast_int(v[0])})
        config['OPTIONS'] = config_options

    if engine:
        config['ENGINE'] = engine
    elif url.scheme in DB_SCHEMES:
        config['ENGINE'] = DB_SCHEMES[url.scheme]

    return config


def _parse_cache(url, backend):
    """Parses a cache configuration url."""

    location = url.netloc.split(',')
    if len(location) == 1:
        location = location[0]

    config = {
        'BACKEND': CACHE_SCHEMES[url.scheme],
        'LOCATION': location,
    }

    if url.scheme == 'filecache':
        config.update({
            'LOCATION': url.netloc + url.path,
        })

    if url.path and url.scheme in ['memcache', 'pymemcache']:
        config.update({
            'LOCATION': 'unix:' + url.path,
        })

    if url.query:
        config_options = {}
        for k, v in urlparse.parse_qs(url.query).items():
            opt = {k.upper(): _cast_int(v[0])}
            if k.upper() in _CACHE_BASE_OPTIONS:
                config.update(opt)
            else:
                config_options.update(opt)
        config['OPTIONS'] = config_options

    if backend:
        config['BACKEND'] = backend

    return config


def parse(url, engine=None):
    """Parses a config URL."""

    if url == 'sqlite://:memory:':
        # this is a special case, because if we pass this URL into
        # urlparse, urlparse will choke trying to interpret "memory"
        # as a port number
        return {
            'ENGINE': DB_SCHEMES['sqlite'],
            'NAME': ':memory:'
        }
        # note: no other settings are required for sqlite

    # otherwise parse the url as normal
    url = urlparse.urlparse(url)

    if url.scheme in DB_SCHEMES or engine in DB_SCHEMES:
        return _parse_db(url, engine)

    if url.scheme in CACHE_SCHEMES:
        return _parse_cache(url, engine)
