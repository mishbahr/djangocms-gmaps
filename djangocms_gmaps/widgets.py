# -*- coding: utf-8 -*-

from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class CoordinatesWidget(forms.TextInput):

    def render(self, name, value, attrs=None):
        output = super(CoordinatesWidget, self).render(name, value, attrs=None)
        return mark_safe(self.format_output(output))

    def format_output(self, rendered_widgets):
        context = {
            'rendered_widgets': rendered_widgets
        }
        return render_to_string('djangocms_gmaps/forms/coordinates_widget.html', context)

    class Media:
        css = {
            'all': ('css/djangocms_gmaps/coordinates_widget.css', )
        }
        js = (
            '//maps.google.com/maps/api/js?sensor=false',
            'js/djangocms_gmaps/coordinates_widget.js',
        )
