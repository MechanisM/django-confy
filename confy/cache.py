# -*- coding: utf-8 -*-
from confy import env, urlparse


CACHE_SCHEMES = {
    'db': 'django.core.cache.backends.db.DatabaseCache',
    'dummy': 'django.core.cache.backends.dummy.DummyCache',
    'file': 'django.core.cache.backends.filebased.FileBasedCache',
    'locmem': 'django.core.cache.backends.locmem.LocMemCache',
    'memcached': 'django.core.cache.backends.memcached.PyLibMCCache',
    'djangopylibmc': 'django_pylibmc.memcached.PyLibMCCache',
    'pymemcached': 'django.core.cache.backends.memcached.MemcachedCache',
    'redis': 'redis_cache.cache.RedisCache',
    'hiredis': 'redis_cache.cache.RedisCache',
    'uwsgi': 'django_uwsgi.cache.UwsgiCache'
}


# Register cache schemes in URLs.
for c in CACHE_SCHEMES.items():
    urlparse.uses_netloc.append(c[0])


def parse_cache_url(url):
    """Parses a cache URL."""
    config = {}

    url = urlparse.urlparse(url)
    # Update with environment configuration.
    config['BACKEND'] = CACHE_SCHEMES[url.scheme]
    if url.scheme in ('file', 'uwsgi'):
        config['LOCATION'] = url.path
        return config
    elif url.scheme in ('redis', 'hiredis'):
        if url.netloc == 'unix':
            location_index = None
            bits = list(filter(None, url.path.split('/')))
            # find the end of the socket path
            for index, bit in enumerate(bits, 1):
                if bit.endswith(('.sock', '.socket')):
                    location_index = index
                    break

            if location_index is None:
                # no socket file extension found, using the whole location
                location = bits
            else:
                # splitting socket path from database and prefix
                location = bits[:location_index]
                rest = bits[location_index:]
                if len(rest) > 0:
                    try:
                        # check if first item of the rest is a database
                        database = int(rest[0])
                        prefix = rest[1:]
                    except ValueError:
                        # or assume the rest is the prefix
                        database = 0
                        prefix = rest
                else:
                    database = prefix = None

            full_location = (url.netloc, '/' + '/'.join(location))
            if database is not None:
                full_location += (str(database),)
            config['LOCATION'] = ':'.join(full_location)
            config['KEY_PREFIX'] = '/'.join(prefix)

        else:
            try:
                userpass, hostport = url.netloc.split('@')
            except ValueError:
                userpass, hostport = '', url.netloc

            try:
                username, password = userpass.split(':')
            except ValueError:
                pass

            path = list(filter(None, url.path.split('/')))
            config['LOCATION'] = ':'.join((hostport, path[0]))
            config['KEY_PREFIX'] = '/'.join(path[1:])

        redis_options = {}

        if url.scheme == 'hiredis':
            redis_options['PARSER_CLASS'] = 'redis.connection.HiredisParser'

        try:
            if password:
                redis_options['PASSWORD'] = password
        except NameError:  # No password defined
            pass

        if redis_options:
            config['OPTIONS'] = redis_options

    else:
        netloc_list = url.netloc.split(',')
        if len(netloc_list) > 1:
            config['LOCATION'] = netloc_list
        else:
            config['LOCATION'] = url.netloc
        config['KEY_PREFIX'] = url.path[1:]

    return config


def config(name='CACHE_URL', default='locmem://'):
    """Returns configured CACHES dictionary from CACHE_URL"""
    config = {}

    s = env(name, default)

    if s:
        config = parse_cache_url(s)

    return config
