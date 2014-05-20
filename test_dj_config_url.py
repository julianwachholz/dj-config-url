# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import unittest

import dj_config_url


POSTGIS_URL = 'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'


class DatabaseTestSuite(unittest.TestCase):

    def test_postgres_parsing(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = dj_config_url.parse(url)

        self.assertEqual(url['ENGINE'], 'django.db.backends.postgresql_psycopg2')
        self.assertEqual(url['NAME'], 'd8r82722r2kuvn')
        self.assertEqual(url['HOST'], 'ec2-107-21-253-135.compute-1.amazonaws.com')
        self.assertEqual(url['USER'], 'uf07k1i6d8ia0v')
        self.assertEqual(url['PASSWORD'], 'wegauwhgeuioweg')
        self.assertEqual(url['PORT'], 5431)

    def test_postgis_parsing(self):
        url = 'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = dj_config_url.parse(url)

        self.assertEqual(url['ENGINE'], 'django.contrib.gis.db.backends.postgis')
        self.assertEqual(url['NAME'], 'd8r82722r2kuvn')
        self.assertEqual(url['HOST'], 'ec2-107-21-253-135.compute-1.amazonaws.com')
        self.assertEqual(url['USER'], 'uf07k1i6d8ia0v')
        self.assertEqual(url['PASSWORD'], 'wegauwhgeuioweg')
        self.assertEqual(url['PORT'], 5431)

    def test_mysql_gis_parsing(self):
        url = 'mysqlgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = dj_config_url.parse(url)

        self.assertEqual(url['ENGINE'], 'django.contrib.gis.db.backends.mysql')
        self.assertEqual(url['NAME'], 'd8r82722r2kuvn')
        self.assertEqual(url['HOST'], 'ec2-107-21-253-135.compute-1.amazonaws.com')
        self.assertEqual(url['USER'], 'uf07k1i6d8ia0v')
        self.assertEqual(url['PASSWORD'], 'wegauwhgeuioweg')
        self.assertEqual(url['PORT'], 5431)

    def test_cleardb_parsing(self):
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = dj_config_url.parse(url)

        self.assertEqual(url['ENGINE'], 'django.db.backends.mysql')
        self.assertEqual(url['NAME'], 'heroku_97681db3eff7580')
        self.assertEqual(url['HOST'], 'us-cdbr-east.cleardb.com')
        self.assertEqual(url['USER'], 'bea6eb025ca0d8')
        self.assertEqual(url['PASSWORD'], '69772142')
        self.assertEqual(url['PORT'], '')

    def test_database_url(self):
        del os.environ['DATABASE_URL']
        a = dj_config_url.config()
        self.assertFalse(a)

        os.environ['DATABASE_URL'] = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'

        url = dj_config_url.config()

        self.assertEqual(url['ENGINE'], 'django.db.backends.postgresql_psycopg2')
        self.assertEqual(url['NAME'], 'd8r82722r2kuvn')
        self.assertEqual(url['HOST'], 'ec2-107-21-253-135.compute-1.amazonaws.com')
        self.assertEqual(url['USER'], 'uf07k1i6d8ia0v')
        self.assertEqual(url['PASSWORD'], 'wegauwhgeuioweg')
        self.assertEqual(url['PORT'], 5431)

    def test_empty_sqlite_url(self):
        url = 'sqlite://'
        url = dj_config_url.parse(url)

        self.assertEqual(url['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(url['NAME'], ':memory:')

    def test_memory_sqlite_url(self):
        url = 'sqlite://:memory:'
        url = dj_config_url.parse(url)

        self.assertEqual(url['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(url['NAME'], ':memory:')

    def test_parse_engine_setting(self):
        engine = 'django_mysqlpool.backends.mysqlpool'
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = dj_config_url.parse(url, engine)

        self.assertEqual(url['ENGINE'], engine)

    def test_config_engine_setting(self):
        engine = 'django_mysqlpool.backends.mysqlpool'
        os.environ['DATABASE_URL'] = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = dj_config_url.config(engine=engine)

        self.assertEqual(url['ENGINE'], engine)

    def test_database_options_parsing(self):
        url = 'postgres://user:pass@host:1234/dbname?conn_max_age=600'
        url = dj_config_url.parse(url)
        self.assertEqual(url['CONN_MAX_AGE'], 600)

        url = 'mysql://user:pass@host:1234/dbname?init_command=SET storage_engine=INNODB'
        url = dj_config_url.parse(url)
        self.assertEqual(url['OPTIONS'], {
            'init_command': 'SET storage_engine=INNODB',
        })


class CacheTestSuite(unittest.TestCase):

    def test_memcache_parsing(self):
        url = 'memcache://127.0.0.1:11211'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'django.core.cache.backends.memcached.MemcachedCache')
        self.assertEqual(url['LOCATION'], '127.0.0.1:11211')

    def test_memcache_pylib_parsing(self):
        url = 'pymemcache://127.0.0.1:11211'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'django.core.cache.backends.memcached.PyLibMCCache')
        self.assertEqual(url['LOCATION'], '127.0.0.1:11211')

    def test_memcache_multiple_parsing(self):
        url = 'memcache://172.19.26.240:11211,172.19.26.242:11212'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'django.core.cache.backends.memcached.MemcachedCache')
        self.assertEqual(url['LOCATION'], ['172.19.26.240:11211', '172.19.26.242:11212'])

    def test_memcache_socket_parsing(self):
        url = 'memcache:///tmp/memcached.sock'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'django.core.cache.backends.memcached.MemcachedCache')
        self.assertEqual(url['LOCATION'], 'unix:/tmp/memcached.sock')

    def test_dbcache_parsing(self):
        url = 'dbcache://my_cache_table'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'django.core.cache.backends.db.DatabaseCache')
        self.assertEqual(url['LOCATION'], 'my_cache_table')

    def test_dbcache_parsing(self):
        url = 'dbcache://my_cache_table'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'django.core.cache.backends.db.DatabaseCache')
        self.assertEqual(url['LOCATION'], 'my_cache_table')

    def test_filecache_parsing(self):
        url = 'filecache:///var/tmp/django_cache'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'django.core.cache.backends.filebased.FileBasedCache')
        self.assertEqual(url['LOCATION'], '/var/tmp/django_cache')

    def test_filecache_windows_parsing(self):
        url = 'filecache://C:/foo/bar'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'django.core.cache.backends.filebased.FileBasedCache')
        self.assertEqual(url['LOCATION'], 'C:/foo/bar')

    def test_locmem_parsing(self):
        url = 'locmemcache://'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'django.core.cache.backends.locmem.LocMemCache')
        self.assertEqual(url['LOCATION'], '')

    def test_locmem_named_parsing(self):
        url = 'locmemcache://unique-snowflake'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'django.core.cache.backends.locmem.LocMemCache')
        self.assertEqual(url['LOCATION'], 'unique-snowflake')

    def test_dummycache_parsing(self):
        url = 'dummycache://'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'django.core.cache.backends.dummy.DummyCache')
        self.assertEqual(url['LOCATION'], '')

    def test_redis_parsing(self):
        url = 'rediscache://127.0.0.1:6379:1?client_class=redis_cache.client.DefaultClient&password=secret'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'redis_cache.cache.RedisCache')
        self.assertEqual(url['LOCATION'], '127.0.0.1:6379:1')
        self.assertEqual(url['OPTIONS'], {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'PASSWORD': 'secret',
        })

    def test_redis_socket_parsing(self):
        url = 'rediscache:///path/to/socket:1'
        url = dj_config_url.parse(url)
        self.assertEqual(url['BACKEND'], 'redis_cache.cache.RedisCache')
        self.assertEqual(url['LOCATION'], 'unix:/path/to/socket:1')

    def test_options_parsing(self):
        url = 'filecache:///var/tmp/django_cache?timeout=60&max_entries=1000&cull_frequency=0'
        url = dj_config_url.parse(url)

        self.assertEqual(url['BACKEND'], 'django.core.cache.backends.filebased.FileBasedCache')
        self.assertEqual(url['LOCATION'], '/var/tmp/django_cache')
        self.assertEqual(url['TIMEOUT'], 60)
        self.assertEqual(url['OPTIONS'], {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 0,
        })

    def test_custom_backend(self):
        url = 'memcache://127.0.0.1:5400?foo=option&bars=9001'
        backend = 'redis_cache.cache.RedisCache'
        url = dj_config_url.parse(url, backend)

        self.assertEqual(url['BACKEND'], backend)
        self.assertEqual(url['LOCATION'], '127.0.0.1:5400')
        self.assertEqual(url['OPTIONS'], {
            'FOO': 'option',
            'BARS': 9001,
        })


if __name__ == '__main__':
    unittest.main()
