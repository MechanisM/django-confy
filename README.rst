Django-Confy
============

Comfy config for Django

Actually this code is just `django-dotenv <https://github.com/jacobian-archive/django-dotenv>`_, `django-getenv <https://github.com/schwuk/django-getenv>`_, `dj-database-url <https://github.com/kennethreitz/dj-database-url>`_, `dj-email-url <https://github.com/migonzalvar/dj-email-url>`_, `dj-search-url <https://github.com/dstufft/dj-search-url>`_ and `django-cache-url <https://github.com/ghickman/django-cache-url>`_ combined together.


Credits
-------

* Code borrowed by `Eugene MechanisM <https://git.io/MechanisM>`_
* Released under `MIT License <http://www.opensource.org/licenses/mit-license.php>`_

Example for settings.py
-----------------------

.. code-block:: py

    ...
    from confy import env, database, cache
    ...
    DEBUG = env('DEV')
    SECRET_KEY = env('SECRET_KEY')
    ...
    DATABASES = {'default': database.config()}
    ...
    CACHES = {'default': cache.config()}

    
Example for .env file
---------------------

.. code-block:: sh

    ...
    DJANGO_SETTINGS_MODULE=project_name.settings
    DEV=True
    DATABASE_URL=sqlite:////server/apps/project_name/project_name.sqlite3
    CACHE_URL=uwsgi://
    ...


Example manage.py
-----------------

.. code-block:: py

    ...
    #!/usr/bin/env python
    import sys
    import confy
    confy.read_environment_file()
    if __name__ == "__main__":
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    ...
 
   
Example for wsgi.py
---------------

.. code-block:: py

    ...
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    ...
