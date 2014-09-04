# -*- coding: utf-8 -*-
from confy import env, urlparse


EMAIL_SCHEMES = {
    'smtp': 'django.core.mail.backends.smtp.EmailBackend',
    'smtps': 'django.core.mail.backends.smtp.EmailBackend',
    'console': 'django.core.mail.backends.console.EmailBackend',
    'file': 'django.core.mail.backends.filebased.EmailBackend',
    'memory': 'django.core.mail.backends.locmem.EmailBackend',
    'dummy': 'django.core.mail.backends.dummy.EmailBackend',
    'uwsgi': 'django_uwsgi.mail.EmailBackend'
}

# Register email schemes in URLs.
for e in EMAIL_SCHEMES.items():
    urlparse.uses_netloc.append(e[0])


def parse_email_url(url):
    """Parses an email URL."""

    conf = {}

    url = urlparse.urlparse(url)

    # Remove query strings
    path = url.path[1:]
    path = path.split('?', 2)[0]

    # Update with environment configuration
    conf.update({
        'EMAIL_FILE_PATH': path,
        'EMAIL_HOST_USER': url.username,
        'EMAIL_HOST_PASSWORD': url.password,
        'EMAIL_HOST': url.hostname,
        'EMAIL_PORT': url.port,
    })

    if url.scheme in EMAIL_SCHEMES:
        conf['EMAIL_BACKEND'] = EMAIL_SCHEMES[url.scheme]

    if url.scheme == 'smtps':
        conf['EMAIL_USE_TLS'] = True
    else:
        conf['EMAIL_USE_TLS'] = False

    return conf


def config(name='EMAIL_URL', default='console://'):
    """Returns a dictionary with EMAIL_* settings from EMAIL_URL."""
    conf = {}
    s = env(name, default)
    if s:
        conf = parse_email_url(s)
    return conf
