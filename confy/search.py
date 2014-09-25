# -*- coding: utf-8 -*-
from confy import env, urlparse


SEARCH_SCHEMES = {
    'elasticsearch': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
    'solr': 'haystack.backends.solr_backend.SolrEngine',
    'whoosh': 'haystack.backends.whoosh_backend.WhooshEngine',
    'simple': 'haystack.backends.simple_backend.SimpleEngine',
    'xapian': 'xapian_backend.XapianEngine'
}

# Register database schemes in URLs.
for s in SEARCH_SCHEMES.items():
    urlparse.uses_netloc.append(s[0])


USES_URL = ["solr"]
USES_INDEX = ["elasticsearch"]
USES_PATH = ["whoosh", "xapian"]


def parse_search_url(url):
    """Parses a search URL."""

    config = {}

    url = urlparse.urlparse(url)

    # Remove query strings.
    path = url.path[1:]
    path = path.split('?', 2)[0]

    if url.scheme in SEARCH_SCHEMES:
        config["ENGINE"] = SEARCH_SCHEMES[url.scheme]

    if url.scheme in USES_URL:
        config["URL"] = urlparse.urlunparse(("http",) + url[1:])

    if url.scheme in USES_INDEX:
        if path.endswith("/"):
            path = path[:-1]

        split = path.rsplit("/", 1)

        if len(split) > 1:
            path = split[:-1]
            index = split[-1]
        else:
            path = ""
            index = split[0]

        config.update({
            "URL": urlparse.urlunparse(("http",) + url[1:2] + (path,) + url[3:]),
            "INDEX_NAME": index,
        })

    if url.scheme in USES_PATH:
        config.update({
            "PATH": path,
        })

    return config


def config(name='SEARCH_URL', default='simple://'):
    """Returns configured SEARCH dictionary from SEARCH_URL"""
    config = {}

    s = env(name, default)

    if s:
        config = parse_search_url(s)

    return config
