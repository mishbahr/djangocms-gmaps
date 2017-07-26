# -*- coding: utf-8 -*-

try:
    from urllib.parse import quote_plus
except ImportError:     # Python 2
    from urllib import quote_plus

from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_spaces_between_tags
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from easy_thumbnails.files import get_thumbnailer
from filer.fields.image import FilerImageField
from jsonfield import JSONField

from .conf import settings


@python_2_unicode_compatible
class Map(CMSPlugin):
    ZOOM_LEVELS = map(lambda c: (c, str(c)), range(22))

    title = models.CharField(
        _('Map Title'), max_length=100, blank=True, null=True)
    width = models.CharField(
        _('Width'), max_length=10, default='100%',
        help_text=_('Map width (in pixels or percent).'))
    height = models.CharField(
        _('Height'), max_length=10, default='400px',
        help_text=_('Map height (in pixels).'))
    zoom = models.PositiveSmallIntegerField(
        _('Zoom Level'), choices=ZOOM_LEVELS, default=13,
        help_text=_('The initial Map zoom level.'))
    map_type = models.CharField(
        _('Map Types'), max_length=50,
        choices=settings.DJANGOCMS_GMAPS_MAP_TYPES,
        default=settings.DJANGOCMS_GMAPS_MAP_TYPES_DEFAULT)
    info_window = models.BooleanField(
        _('Info window'), default=True,
        help_text=_('Show textbox over marker?'))
    scrollwheel = models.BooleanField(
        _('Scrollwheel'), default=True,
        help_text=_('If false, disables scrollwheel zooming on the map. '
                    'The scrollwheel is enabled by default.'))
    double_click_zoom = models.BooleanField(
        _('Disable Double Click Zoom'), default=False,
        help_text=_('Enables/disables zoom and center on double click.'
                    ' Enabled by default.'))
    draggable = models.BooleanField(
        _('Draggable'), default=True,
        help_text=_('If false, prevents the map from being dragged. '
                    'Dragging is enabled by default.'))
    keyboard_shortcuts = models.BooleanField(
        _('Keyboard Shortcuts'), default=True,
        help_text=_('If false, prevents the map from being controlled by the '
                    'keyboard. Keyboard shortcuts are enabled by default.'))
    pan_control = models.BooleanField(
        _('Pan control'), default=True,
        help_text=_('The Pan control displays buttons for panning the map. '))
    zoom_control = models.BooleanField(
        _('Zoom Control'), default=True,
        help_text=_('The Zoom control displays a slider (for large maps) or '
                    'small \'+/-\' buttons (for small maps) to control the '
                    'zoom level of the map. '))
    street_view_control = models.BooleanField(
        _('Street View Control'), default=True,
        help_text=_('The Street View control contains a Pegman icon which '
                    'can be dragged onto the map to enable Street View.'))
    map_type_control = models.BooleanField(
        _('Map Type Control'), default=True,
        help_text=_('The MapType control lets the user toggle between '
                    'map types (such as ROADMAP and SATELLITE).'))

    styles = JSONField(_('Map Style'), blank=True, null=True)

    plugin_template = models.CharField(
        _('Template'), max_length=255,
        choices=settings.DJANGOCMS_GMAPS_TEMPLATES,
        default=settings.DJANGOCMS_GMAPS_TEMPLATES[0][0],
    )

    def get_map_styles(self):
        if not self.styles:
            return []
        return self.styles

    def __str__(self):
        if self.child_plugin_instances:
            num_children = len(self.child_plugin_instances)
            return u'%s location%s' % (num_children, 's'[num_children == 1:])
        return u'Please add a location'


@python_2_unicode_compatible
class Location(CMSPlugin):
    location_name = models.CharField(_('Name'), max_length=255, blank=True, null=True)
    street_address = models.CharField(
        _('Street Address'), max_length=150, blank=True,
        help_text=_('The street address. e.g 121 High Street or High St'))
    locality = models.CharField(_('City/Town'), max_length=100, blank=True)
    region = models.CharField(
        _('Region'), max_length=100, blank=True)
    postal_code = models.CharField(_('Postcode'), max_length=30, blank=True)
    country_short = models.CharField(
        _('Country'), max_length=255, blank=True, choices=settings.DJANGOCMS_GMAPS_COUNTRIES)
    formatted_address = models.CharField(
        _('Formatted Address'), max_length=255, blank=True,
        help_text=_('Human-readable address of this location.'))
    coordinates = models.CharField(
        _('Coordinates'), max_length=255,
        help_text=_('Drag map marker to fine tune the map position.'))
    photo = FilerImageField(
        verbose_name=_('Location Photo'), blank=True, null=True,
        on_delete=models.SET_NULL, related_name='djangocms_map_locations')
    infowindow = models.TextField(_('Content'), blank=True)
    marker_icon = FilerImageField(
        verbose_name=_('Marker Icon'), blank=True, null=True,
        on_delete=models.SET_NULL, related_name='djangocms_map_marker_icons')

    @property
    def country(self):
        return self.get_country_code_display()

    @property
    def address_components(self):
        address_fields = ['street_address', 'locality', 'region', 'postal_code', 'country']
        address_components = []
        for field in address_fields:
            if getattr(self, field, None):
                address_components.append(getattr(self, field).strip())
        return address_components

    @property
    def address(self):
        if self.formatted_address:
            return self.formatted_address
        return ', '.join(self.address_components)

    def get_marker_icon(self):
        if not self.marker_icon or not settings.DJANGOCMS_GMAPS_CUSTOM_MARKERS_ENABLED:
            return ''

        thumbnailer = get_thumbnailer(self.marker_icon)
        thumb = thumbnailer.get_thumbnail({
            'size': (
                settings.DJANGOCMS_GMAPS_CUSTOM_MARKERS_WIDTH,
                settings.DJANGOCMS_GMAPS_CUSTOM_MARKERS_HEIGHT
            )
        })
        return thumb.url

    def get_infowindow(self):
        if not self.infowindow or not settings.DJANGOCMS_GMAPS_INFOWINDOW_ENABLED:
            return ''

        rendered_infowindow = render_to_string(
            settings.DJANGOCMS_GMAPS_INFOWINDOW_TEMPLATE, {'location': self, })
        return {
            'content': strip_spaces_between_tags(rendered_infowindow.strip()),
            'maxWidth': settings.DJANGOCMS_GMAPS_INFOWINDOW_MAXWIDTH
        }

    def get_coordinates(self):
        coordinates = [pos.strip() for pos in self.coordinates.split(',')]
        return coordinates[0], coordinates[1]

    @property
    def edit_plugin_url(self):
        return reverse('admin:cms_page_edit_plugin', args=[self.pk])

    @property
    def get_direction_url(self):
        coordinates = self.get_coordinates()
        params = {
            'zoom': 17,
            'lat': coordinates[0],
            'lng': coordinates[1],
            'address': quote_plus(self.address.encode('utf-8'))
        }
        return u'http://maps.google.com/maps' \
               u'?f=d&z=%(zoom)s&ll=%(lat)s,%(lng)s' \
               u'&daddr=%(address)s' % params

    def __str__(self):
        if self.location_name:
            return u'%s (%s)' % (self.location_name, self.address)
        return u'%s' % self.address
