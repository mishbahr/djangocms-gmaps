=============================
djangocms-gmaps
=============================

.. image:: http://img.shields.io/pypi/v/djangocms-gmaps.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-gmaps/
    :alt: Latest Version

.. image:: http://img.shields.io/pypi/dm/djangocms-gmaps.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-gmaps/
    :alt: Downloads

.. image:: http://img.shields.io/pypi/l/djangocms-gmaps.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-gmaps/
    :alt: License

.. image:: https://img.shields.io/badge/django--cms-3.0-blue.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-cms/
    :alt: django-cms
    
    

The easiest way to embed Google Maps for your django-cms powered site - includes a custom ``CoordinatesWidget`` widget with draggable marker to fine tune map positions. This is a great way to display the location of your business or event. This project requires django-cms v3.0 or higher to be properly installed and configured. 


Quickstart
----------

1. Install `djangocms-gmaps`::

    pip install djangocms-gmaps

2. Add `djangocms_gmaps` to `INSTALLED_APPS`::

    INSTALLED_APPS = (
        ...
        'djangocms_gmaps',
        ...
    )



Configuration
-------------

Plugin(s) Module — If module is None, plugin is grouped ``Generic`` group::

     DJANGOCMS_GMAPS_PLUGIN_MODULE = _('Generic')

Name of the ``Map`` plugin::

    DJANGOCMS_GMAPS_PLUGIN_NAME = _('Map')

Name of the ``Location`` plugin::

    DJANGOCMS_GMAPS_LOCATION_PLUGIN_NAME = _('Location')

Can this plugin only be attached to a placeholder that is attached to a page::
    
   DJANGOCMS_GMAPS_PAGE_ONLY = False

A list of Plugin Class Names. If this is set, this plugin may only be added to plugins listed here::

    DJANGOCMS_GMAPS_PARENT_CLASSES = None

Is it required that this plugin is a child of another plugin? Or can it be added to any placeholder::

    DJANGOCMS_GMAPS_REQUIRE_PARENT = False

Whether this plugin can be used in text plugins or not::

    DJANGOCMS_GMAPS_TEXT_ENABLED = False

The path to the template used to render the template::

    DJANGOCMS_GMAPS_TEMPLATE = 'djangocms_gmaps/default.html'

You can customize the content and appearance of ``InfoWindow`` attached to map markers::

    DJANGOCMS_GMAPS_INFOWINDOW_TEMPLATE = 'djangocms_map/infowindow.html'

Set fieldsets to control the layout of ``Map`` plugin add/change form::

    DJANGOCMS_GMAPS_FIELDSETS = None

Set fieldsets to control the layout of ``Location`` plugin add/change form::

    DJANGOCMS_GMAPS_LOCATION_FIELDSETS = None

