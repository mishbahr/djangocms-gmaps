(function($) {
    $(function() {
        var map = null,
            markers = [],
            coordinatesInput = $('input[name="coordinates"]'),
            addressComponents = $(
                'input[name="street_address"], input[name="locality"], input[name="region"], input[name="postal_code"], select[name="country_short"]'
            );

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
            console.log('GMAP initialize');
            var mapOptions = {
                center: new google.maps.LatLng(40.712784, -74.005941),
                zoom: 11,
                mapTypeControl: false,
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
            'JavaScript library http://maps.google.com/maps/api/js'
        } else {
            google.maps.event.addDomListener(window, 'load', initialize);
        }

    });
})(django.jQuery);
