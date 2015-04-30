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

.. image:: http://mishbahr.github.io/djangocms-gmaps/assets/djangocms_gmaps_001.png
  :target: http://mishbahr.github.io/djangocms-gmaps/assets/djangocms_gmaps_001.png
  :width: 768px
  :align: center


The easiest way to embed Google Maps for your ``django-cms`` powered site - includes a custom ``CoordinatesWidget`` with draggable marker to fine tune map positions. This project requires django-cms v3.0 or higher to be properly installed and configured. 


Preview
--------

.. image:: http://mishbahr.github.io/djangocms-gmaps/assets/djangocms_gmaps_002.png
  :target: http://mishbahr.github.io/djangocms-gmaps/assets/djangocms_gmaps_002.png
  :width: 768px
  :align: center
  
.. image:: http://mishbahr.github.io/djangocms-gmaps/assets/djangocms_gmaps_003.png
  :target: http://mishbahr.github.io/djangocms-gmaps/assets/djangocms_gmaps_003.png
  :width: 768px
  :align: center

Quickstart
----------

1. Install ``djangocms-gmaps``::

    pip install djangocms-gmaps

2. Add ``djangocms_gmaps`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'djangocms_gmaps',
        ...
    )

3. Sync the models with database::

    python manage.py migrate

  
Configuration
-------------

Plugin(s) Module - If module is None, plugin is grouped ``Generic`` group::

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

Enable ``Advanced Options`` to allow the users to fully customise map controls e.g. ``streetViewControl``::

    DJANGOCMS_GMAPS_ADVANCED_OPTIONS_ENABLED = True

Styled maps allow the user to customize the presentation of the Google maps, changing the visual display of such elements as roads, parks, and built-up areas::

   DJANGOCMS_GMAPS_STYLED_MAPS_ENABLED = True

Info windows - set this to false if you want to disable the infowindow::

    DJANGOCMS_GMAPS_INFOWINDOW_ENABLED = True


Info window with maxWidth - the maximum width of  a info window is set to 220 pixels::

    DJANGOCMS_GMAPS_INFOWINDOW_MAXWIDTH = 220

Allow users to define custom marker icons for individual locations instead of the default icons:: 

    DJANGOCMS_GMAPS_CUSTOM_MARKERS_ENABLED = True 


