Usage
~~~~~


Import from confy needed modules and use them.
Example for settings.py:

.. code-block:: py

    from confy import env, database, cache

    DEBUG = env('DEV')
    SECRET_KEY = env('SECRET_KEY')

    DATABASES = {'default': database.config()}

    CACHES = {'default': cache.config()}

    
Create .env file and place it into project's root directory(where manage.py is located)
And add into it environment variable like these:

.. code-block:: sh

    DJANGO_SETTINGS_MODULE=project_name.settings
    DEV=True
    DATABASE_URL=sqlite:////server/apps/project_name/project_name.sqlite3
    CACHE_URL=uwsgi://


Modify your manage.py file to read environment variables(if you don't read them other ways like honcho, uwsgi etc.)

.. code-block:: py

    #!/usr/bin/env python
    import sys
    import confy
    confy.read_environment_file()
    if __name__ == "__main__":
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
 

Since environment variables exists you don't need to use os.environ.setdefault for wsgi.py and manage.py

.. code-block:: py

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
