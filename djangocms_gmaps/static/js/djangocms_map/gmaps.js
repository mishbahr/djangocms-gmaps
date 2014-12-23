if (!(typeof window.google === 'object' && window.google.maps)) {
  throw 'Google Maps API is required. Please register the following JavaScript library ' +
  'http://maps.google.com/maps/api/js?sensor=true.'
}

var extendObject = function(obj, new_obj) {
  if (obj === new_obj) {
    return obj;
  }

  for (var name in new_obj) {
    obj[name] = new_obj[name];
  }
  return obj;
};

var coordinatesToLatlng = function(coordinates) {
  var lat = coordinates[0],
    lng = coordinates[1];
  return new google.maps.LatLng(lat, lng);
};

var getElementById = function(id) {
  id = id.replace('#', '');
  return document.getElementById(id);
};

var getDataAttribute = function(elem, key) {
  var data = elem.getAttribute('data-' + key);
  return window.JSON.parse(data)[0];
};

var GMaps = function(options) {
  options.mapType = options.mapType || 'roadmap';

  var that = this,
    container_id = options.el || options.div,
    mapCenter = new google.maps.LatLng(37.4419, -122.1419),
    el = typeof container_id == 'string' ? getElementById(container_id) : container_id,
    locations = options.locations,
    markers = [];


  var fitZoom = function() {
    var latLngs = [];
    for (var i = 0; i < markers.length; i++) {
      if (typeof(markers[i].visible) === 'boolean' && markers[i].visible) {
        latLngs.push(markers[i].getPosition());
      }
    }

    fitLatLngBounds(latLngs);
  };

  var fitLatLngBounds = function(latLngs) {
    var total = latLngs.length;
    var bounds = new google.maps.LatLngBounds();

    for (var i = 0; i < total; i++) {
      bounds.extend(latLngs[i]);
    }

    map.fitBounds(bounds);
  };

  var setCenter = function(lat, lng) {
    map.panTo(new google.maps.LatLng(lat, lng));
  };

  var hideInfoWindows = function() {
    for (var i = 0; i < markers.length; i++){
      if (markers[i].infoWindow) {
        markers[i].infoWindow.close();
      }
    };
  };

  var addMarker = function(options) {
    var markerOptions = {
      position: coordinatesToLatlng(options.coordinates),
      title: options.address,
      animation: google.maps.Animation.DROP,
      map: null,
      icon: options.icon
    };

    var marker = new google.maps.Marker(markerOptions);

    if (options.infoWindow) {
      marker.infoWindow = new google.maps.InfoWindow({
        content: options.infoWindow.content,
        maxWidth: options.infoWindow.maxWidth
      });
      google.maps.event.addListener(marker, 'click', function() {
          hideInfoWindows();
					marker.infoWindow.open(map, marker);
			});
    };
    markers.push(marker);
    marker.setMap(map);
  };

  if (typeof(el) === 'undefined' || el === null) {
    throw 'Map error: Can\'t find map container.';
  }

  if (options.locations.length > 0) {
    mapCenter = coordinatesToLatlng(locations[0].coordinates);
  }

  var mapOptions = {
    center: mapCenter,
    disableDoubleClickZoom: options.disableDoubleClickZoom,
    draggable: options.draggable,
    keyboardShortcuts: options.keyboardShortcuts,
    mapTypeControl: options.mapTypeControl,
    mapTypeId: google.maps.MapTypeId[options.mapType.toUpperCase()],
    panControl: options.panControl ,
    scrollwheel: options.scrollwheel,
    streetViewControl: options.streetViewControl,
    styles: options.styles,
    zoom: options.zoom,
    zoomControl: options.zoomControl
  };

  el.style.width = options.width;
  el.style.height = options.height;

  var map = new google.maps.Map(el, mapOptions);

  for (var i = 0; i < locations.length; i++) {
    addMarker(locations[i]);
  }
  if (locations.length > 1){
    fitZoom();
  }
};

google.maps.event.addDomListener(window, 'load', function() {
  var maps = document.getElementsByClassName('djangocms-map');
  for (var i = 0; i < maps.length; i++) {
    var mapOptions = {
      div: maps[i]
    };
    mapOptions = extendObject(mapOptions, getDataAttribute(maps[i], 'options'));
    new GMaps(mapOptions);
  }
});
