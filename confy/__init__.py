__version__ = '1.0.4'
import os
import sys
import warnings
import ast

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse



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
        raise Exception("Missing required environment variable '%s'" % key)


default_app_config = 'confy.apps.ConfyConfig'
