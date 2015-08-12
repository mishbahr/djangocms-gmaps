#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import djangocms_gmaps

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = djangocms_gmaps.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()

setup(
    name='djangocms-gmaps',
    version=version,
    description="""The easiest way to embed Google Maps for your django-cms powered site. This is a great way to display the location of your business or event.""",
    long_description=readme,
    author='Mishbah Razzaque',
    author_email='mishbahx@gmail.com',
    url='https://github.com/mishbahr/djangocms-gmaps',
    packages=[
        'djangocms_gmaps',
    ],
    include_package_data=True,
    install_requires=[
        'django-appconf',
        'jsonfield',
        'django-cms>=3.0',
        'django-filer>=0.9',
        'easy-thumbnails>=1.0',
        'django-sekizai>=0.7',
    ],
    license="BSD",
    zip_safe=False,
    keywords='djangocms-gmaps, django-cms, djangocms-googlemap, google maps, django',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)