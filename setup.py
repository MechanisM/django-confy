import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

from confy import __version__



os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name="django-confy",
    version=__version__,
    description="Django project configuration helpers",
    long_description=open('README.rst').read(),
    url='http://github.com/MechanisM/django-confy',
    author='Eugene MechanisM',
    author_email='eugene@mechanism.name',
    license='MIT',
    zip_safe = False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='django, config, env, 12factor',
    packages=find_packages(),
    include_package_data=True,
)
