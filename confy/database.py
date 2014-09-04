# -*- coding: utf-8 -*-
import urlparse
from confy import env


DATABASE_SCHEMES = {
    'postgres': 'django.db.backends.postgresql_psycopg2',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'postgis': 'django.contrib.gis.db.backends.postgis',
    'mysql': 'django.db.backends.mysql',
    'mysql2': 'django.db.backends.mysql',
    'sqlite': 'django.db.backends.sqlite3'
}

# Register database schemes in URLs.
for i in DATABASE_SCHEMES.items():
    urlparse.uses_netloc.append(i[0])


def parse_database_url(url):
    """Parses a database URL."""

    if url == 'sqlite://:memory:':
        # this is a special case, because if we pass this URL into
        # urlparse, urlparse will choke trying to interpret "memory"
        # as a port number
        return {
            'ENGINE': DATABASE_SCHEMES['sqlite'],
            'NAME': ':memory:'
        }
        # note: no other settings are required for sqlite

    # otherwise parse the url as normal
    config = {}

    url = urlparse.urlparse(url)

    # Remove query strings.
    path = url.path[1:]
    path = path.split('?', 2)[0]

    # if we are using sqlite and we have no path, then assume we
    # want an in-memory database (this is the behaviour of sqlalchemy)
    if url.scheme == 'sqlite' and path == '':
        path = ':memory:'

    # Update with environment configuration.
    config.update({
        'NAME': path,
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
    })

    if url.scheme in DATABASE_SCHEMES:
        config['ENGINE'] = DATABASE_SCHEMES[url.scheme]

    return config


def config(name='DATABASE_URL', default='sqlite://:memory:'):
    """Returns configured DATABASE dictionary from DATABASE_URL."""
    config = {}
    s = env(name, default)
    if s:
        config = parse_database_url(s)
    return config
