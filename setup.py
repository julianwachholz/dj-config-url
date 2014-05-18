# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='dj-config-url',
    version='0.1.1',
    url='https://github.com/julianwachholz/dj-config-url',
    license='BSD',
    author='Julian Wachholz',
    author_email='julian@wachholz.ch',
    description='Use configuration URLs in your Django Application.',
    long_description=open('README.rst').read(),
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
