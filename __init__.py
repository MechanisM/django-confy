__version__ = '1.0.2'
import os
import sys
import warnings
import ast
from urllib.parse import urlparse
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings



def setting(key, default=None, required=False):
    try:
        value = getattr(settings, key, default)
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
    except KeyError:
        if default or not required:
            return default
        raise ImproperlyConfigured("Missing required setting variable '%s'" % key)


# from django.utils.importlib import import_module
# from django.utils.module_loading import module_has_submodule
#
#
#
# def autoload(submodules):
#     for app in settings.INSTALLED_APPS:
#         mod = import_module(app)
#         for submodule in submodules:
#             try:
#                 import_module("{0}.{1}".format(app, submodule))
#             except:
#                 if module_has_submodule(mod, submodule):
#                     raise
#
#
# def run():
#     autoload(["receivers"])


def parse_environment_file(envfile):
    for line in open(envfile):
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        v = v.strip("'").strip('"')
        yield k, v


def read_environment_file(envfile=None):
    """
    Read a .env file into os.environ.

    If not given a path to a envfile path, does filthy magic stack backtracking
    to find manage.py and then find the envfile.
    """
    if envfile is None:
        frame = sys._getframe()
        envfile = os.path.join(os.path.dirname(frame.f_back.f_code.co_filename), '.env')
        if not os.path.exists(envfile):
            warnings.warn("not reading %s - it doesn't exist." % envfile)
            return
    for k, v in parse_environment_file(envfile):
        os.environ.setdefault(k, v)


def env(key, default=None, required=False):
    """
    Retrieves environment variables and returns Python natives. The (optional)
    default will be returned if the environment variable does not exist.
    """
    try:
        value = os.environ[key]
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
    except KeyError:
        if default or not required:
            return default
        raise ImproperlyConfigured("Missing required environment variable '%s'" % key)


class Path(object):
    """Inspired to Django Two-scoops, handling File Paths in Settings.

>>> from environ import Path
>>> root = Path('/home')
>>> root, root(), root('dev')
(<Path:/home>, '/home', '/home/dev')
>>> root == Path('/home')
True
>>> root in Path('/'), root not in Path('/other/path')
(True, True)
>>> root('dev', 'not_existing_dir', required=True)
Traceback (most recent call last):
environ.environ.ImproperlyConfigured: Create required path: /home/not_existing_dir
>>> public = root.path('public')
>>> public, public.root, public('styles')
(<Path:/home/public>, '/home/public', '/home/public/styles')
>>> assets, scripts = public.path('assets'), public.path('assets', 'scripts')
>>> assets.root, scripts.root
('/home/public/assets', '/home/public/assets/scripts')
>>> assets + 'styles', str(assets + 'styles'), ~assets
(<Path:/home/public/assets/styles>, '/home/public/assets/styles', <Path:/home/public>)

"""

    def path(self, *paths, **kwargs):
        """Create new Path based on self.root and provided paths.

:param paths: List of sub paths
:param kwargs: required=False
:rtype: Path
"""
        return self.__class__(self.__root__, *paths, **kwargs)

    def file(self, name, *args, **kwargs):
        """Open a file.

:param name: Filename appended to self.root
:param args: passed to open()
:param kwargs: passed to open()

:rtype: file
"""
        return open(self(name), *args, **kwargs)

    @property
    def root(self):
        """Current directory for this Path"""
        return self.__root__

    def __init__(self, start='', *paths, **kwargs):

        super(Path, self).__init__()

        if kwargs.get('is_file', False):
            start = os.path.dirname(start)

        self.__root__ = self._absolute_join(start, *paths, **kwargs)

    def __call__(self, *paths, **kwargs):
        """Retrieve the absolute path, with appended paths

:param paths: List of sub path of self.root
:param kwargs: required=False
"""
        return self._absolute_join(self.__root__, *paths, **kwargs)

    def __eq__(self, other):
        return self.__root__ == other.__root__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return Path(self.__root__, other if not isinstance(other, Path) else other.__root__[1:])

    def __sub__(self, other):
        if isinstance(other, int):
            return self.path('../' * other)
        raise TypeError("unsupported operand type(s) for -: 'str' and '{0}'".format(other.__class__.__name__))

    def __invert__(self):
        return self.path('..')

    def __contains__(self, item):
        base_path = self.__root__
        if len(base_path) > 1:
            base_path += '/'
        return item.__root__.startswith(base_path)

    def __repr__(self):
        return "<Path:{0}>".format(self.__root__)

    def __str__(self):
        return self.__root__

    def __unicode__(self):
        return self.__str__()

    @staticmethod
    def _absolute_join(base, *paths, **kwargs):
        absolute_path = os.path.abspath(os.path.join(base, *paths))
        if kwargs.get('required', False) and not os.path.exists(absolute_path):
            raise ImproperlyConfigured("Create required path: {0}".format(absolute_path))
        return absolute_path


default_app_config = 'confy.apps.ConfyConfig'
