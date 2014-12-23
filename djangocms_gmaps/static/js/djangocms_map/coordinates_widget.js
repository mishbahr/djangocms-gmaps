(function($) {
    $(function() {
        var map = null,
            markers = [],
            coordinatesInput = $('input[name="coordinates"]'),
            addressComponents = $(
                'input[name="street_address"], input[name="locality"], input[name="region"], input[name="postal_code"], select[name="country_short"]'
            ),
            styles = [{
                "featureType": "landscape",
                "stylers": [{
                    "saturation": -100
                }, {
                    "lightness": 65
                }, {
                    "visibility": "on"
                }]
            }, {
                "featureType": "poi",
                "stylers": [{
                    "saturation": -100
                }, {
                    "lightness": 51
                }, {
                    "visibility": "simplified"
                }]
            }, {
                "featureType": "road.highway",
                "stylers": [{
                    "saturation": -100
                }, {
                    "visibility": "simplified"
                }]
            }, {
                "featureType": "road.arterial",
                "stylers": [{
                    "saturation": -100
                }, {
                    "lightness": 30
                }, {
                    "visibility": "on"
                }]
            }, {
                "featureType": "road.local",
                "stylers": [{
                    "saturation": -100
                }, {
                    "lightness": 40
                }, {
                    "visibility": "on"
                }]
            }, {
                "featureType": "transit",
                "stylers": [{
                    "saturation": -100
                }, {
                    "visibility": "simplified"
                }]
            }, {
                "featureType": "administrative.province",
                "stylers": [{
                    "visibility": "off"
                }]
            }, {
                "featureType": "water",
                "elementType": "labels",
                "stylers": [{
                    "visibility": "on"
                }, {
                    "lightness": -25
                }, {
                    "saturation": -100
                }]
            }, {
                "featureType": "water",
                "elementType": "geometry",
                "stylers": [{
                    "hue": "#ffff00"
                }, {
                    "lightness": -25
                }, {
                    "saturation": -97
                }]
            }];

        var addressOnChange = function() {
            var address = addressComponents.map(function() {
                return $.trim($(this).val());
            }).get().join(', ');

            var geocoder = new google.maps.Geocoder();
            geocoder.geocode({
                'address': address
            }, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    var latlng = results[0].geometry.location;
                    coordinatesInput.val(latlng.lat() + ', ' + latlng.lng()).trigger('change');
                }
            });

        };

        var placeMarker = function() {
            // clear markers.
            for (var i = 0; i < markers.length; i++) {
                markers[i].setMap(null);
            }
            markers = [];

            var latlng = $.map(coordinatesInput.val().split(','), $.trim);
            var position = new google.maps.LatLng(latlng[0], latlng[1]);

            var marker = new google.maps.Marker({
                position: position,
                draggable: true,
                animation: google.maps.Animation.DROP,
                map: map
            });

            markers.push(marker);

            map.setCenter(position);
            map.setZoom(16);

            google.maps.event.addListener(marker, 'dragend', function() {
                var position = marker.getPosition();
                coordinatesInput.val(position.lat() + ', ' + position.lng());
                map.setCenter(position);
            });
        };

        var initialize = function() {
            var mapOptions = {
                center: new google.maps.LatLng(40.712784, -74.005941),
                zoom: 11,
                styles: styles
            };
            map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
            if (coordinatesInput.val()) {
                placeMarker();
            }
            addressComponents.on('change', addressOnChange);
            coordinatesInput.on('change', placeMarker);

        };

        if (!(typeof window.google === 'object' && window.google.maps)) {
            throw 'Google Maps API is required. Please register the following ' +
            'JavaScript library http://maps.google.com/maps/api/js?sensor=true.'
        } else {
            google.maps.event.addDomListener(window, 'load', initialize);
        }

    });
})(django.jQuery);
