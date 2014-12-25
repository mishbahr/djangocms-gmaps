try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .conf import settings
from .widgets import CoordinatesWidget
from .models import Map, Location


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        widgets = {
            'coordinates': CoordinatesWidget(),
        }


class LocationPlugin(CMSPluginBase):
    model = Location
    form = LocationForm
    module = settings.DJANGOCMS_GMAPS_PLUGIN_MODULE
    name = settings.DJANGOCMS_GMAPS_LOCATION_PLUGIN_NAME
    render_plugin = False
    parent_classes = ('MapPlugin', )

    def get_fieldsets(self, request, obj=None):
        if settings.DJANGOCMS_GMAPS_LOCATION_FIELDSETS:
            return settings.DJANGOCMS_GMAPS_LOCATION_FIELDSETS

        fieldsets = (
            (None, {
                'fields': ('location_name', 'street_address', 'locality',
                           'region', 'postal_code', 'country_short',
                           'coordinates', 'formatted_address', )
            }),

        )

        if settings.DJANGOCMS_GMAPS_INFOWINDOW_ENABLED:
            fieldsets = fieldsets + (
                (_('Info Window'), {
                    'classes': ('collapse', ),
                    'fields': ('photo', 'infowindow', )
                }),
            )

        if settings.DJANGOCMS_GMAPS_CUSTOM_MARKERS_ENABLED:
            fieldsets = fieldsets + (
                (_('Custom Markers'), {
                    'classes': ('collapse', ),
                    'description': 'Display a different image in place of '
                                   'the default Google map marker pin',
                    'fields': ('marker_icon', )
                }),
            )

        return fieldsets

plugin_pool.register_plugin(LocationPlugin)


class MapPlugin(CMSPluginBase):
    model = Map
    module = settings.DJANGOCMS_GMAPS_PLUGIN_MODULE
    name = settings.DJANGOCMS_GMAPS_PLUGIN_NAME
    render_template = settings.DJANGOCMS_GMAPS_TEMPLATE
    child_classes = ('LocationPlugin', )
    allow_children = True

    def get_fieldsets(self, request, obj=None):
        if settings.DJANGOCMS_GMAPS_FIELDSETS:
            return settings.DJANGOCMS_GMAPS_FIELDSETS

        fieldsets = (
            (None, {
                'fields': ('title', )
            }),
            (None, {
                'fields': ('width', 'height', 'zoom', 'map_type', )
            }),
        )

        if settings.DJANGOCMS_GMAPS_ADVANCED_OPTIONS_ENABLED:
            fieldsets = fieldsets + (
                (_('Advanced Options'), {
                    'classes': ('collapse', ),
                    'fields': ('info_window', 'scrollwheel', 'double_click_zoom', 'draggable',
                               'keyboard_shortcuts', 'pan_control', 'zoom_control',
                               'street_view_control', 'map_type_control', ),
                }),
            )

        if settings.DJANGOCMS_GMAPS_STYLED_MAPS_ENABLED:
            fieldsets = fieldsets + (
                (_('Style Options'), {
                    'classes': ('collapse', ),
                    'fields': ('styles',)
                }),
            )

        return fieldsets

    def get_locations(self, instance):
        locations = []
        child_plugins = getattr(instance, 'child_plugin_instances', None) or []
        for location in child_plugins:
            locations.append({
                'title': location.location_name.strip(),
                'address': location.address,
                'coordinates': location.get_coordinates(),
                'get_direction_url': location.get_direction_url,
                'edit_plugin_url': location.edit_plugin_url,
                'icon': location.get_marker_icon(),
                'infoWindow': location.get_infowindow(),
            })
        return locations

    def get_map_options(self, context, instance):
        options = {
            'zoom': instance.zoom,
            'mapType': instance.map_type,
            'scrollwheel': instance.scrollwheel,
            'disableDoubleClickZoom': instance.double_click_zoom,
            'draggable': instance.draggable,
            'keyboardShortcuts': instance.keyboard_shortcuts,
            'panControl': instance.pan_control,
            'zoomControl': instance.zoom_control,
            'streetViewControl': instance.street_view_control,
            'mapTypeControl': instance.map_type_control,
            'width': instance.width,
            'height': instance.height,
            'styles': instance.get_map_styles(),
            'locations': self.get_locations(instance),
            'edit_mode': context['request'].toolbar.edit_mode
        }
        return options

    def render(self, context, instance, placeholder):
        context = super(MapPlugin, self).render(context, instance, placeholder)
        map_options = self.get_map_options(context, instance),
        context.update({
            'map_options': mark_safe(json.dumps(map_options))
        })
        return context


plugin_pool.register_plugin(MapPlugin)
