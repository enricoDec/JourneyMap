var markers = [];
var polyline;

function create_map(data) {
    var json = JSON.parse(data);

    var locations = json.map(element => element[1]);

    var bounds = get_bounds(locations);
    var center = get_map_center(bounds);

    var map = L.map("map", {
        center: center,
        crs: L.CRS.EPSG3857,
        maxBounds: [[-90, -180], [90, 180]],
        zoom: 10,
        zoomControl: true,
        preferCanvas: false,
    });
    
    map.fitBounds(bounds);

    var tile_layer = L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            "attribution": "Data by &copy; \<a href=\"http://openstreetmap.org\">OpenStreetMap</a>, under <a href=\"http://www.openstreetmap.org/copyright\">ODbL</a>.",
            "detectRetina": false,
            "maxNativeZoom": 18,
            "maxZoom": 18,
            "minZoom": 3,
            "noWrap": false,
            "opacity": 1,
            "subdomains":
            "abc",
            "tms": false
        }
    ).addTo(map);

    place_markers(json.slice(), map);
    
    map.on('zoomend', function() {
        remove_markers();
        place_markers(json.slice(), map);
    });
}

function get_map_center(bounds) {
    return [(bounds[0][0] + bounds[1][0]) / 2, (bounds[0][1] + bounds[1][1]) / 2];
}

function get_bounds(locations) {
    var bounds = [[Number.MAX_VALUE, Number.MAX_VALUE], [Number.MIN_VALUE, Number.MIN_VALUE]];

    locations.forEach(element => {
        bounds = [
            [
                Math.min(bounds[0][0], element[0]),
                Math.min(bounds[0][1], element[1]),
            ],
            [
                Math.max(bounds[1][0], element[0]),
                Math.max(bounds[1][1], element[1]),
            ],
        ]
    });

    return bounds;
}

function place_markers(json_data, map) {
    var combined_json_data = combine_markers(json_data, map);

    var refactored_markers = refactor_markers(combined_json_data[0]);
    var refactored_waypoints = refactor_waypoints(combined_json_data[1], refactored_markers);

    //console.log(refactored_waypoints);

    polyline = L.polyline(
        refactored_waypoints,
        {
            "bubblingMouseEvents": true,
            "color": "#212529",
            "dashArray": null,
            "dashOffset": null,
            "fill": false,
            "fillColor":
            "#3388ff",
            "fillOpacity": 0.2,
            "fillRule": "evenodd",
            "lineCap": "round",
            "lineJoin": "round",
            "noClip": false,
            "opacity": 1.0,
            "smoothFactor": 1.0,
            "stroke": true,
            "weight": 2
        }).addTo(map);


    
    var distanceParagraph = document.getElementById("distance-paragraph");
    var distance = get_distance_of_journey(refactored_waypoints);
    distanceParagraph.innerText = distance >= 1000.0 ? (distance / 1000.0).toFixed(3) + " km" : distance.toFixed(0) + " m";

    var marker_radius = 25;

    var CircleImageIcon = L.Icon.extend({
        options: {                    
            iconSize: [marker_radius * 2, marker_radius * 2],
            iconAnchor: [marker_radius, marker_radius],
            popupAnchor: [0, -marker_radius]
        }
    });

    refactored_markers.forEach(element => {
        var marker = L.marker(
            element[1], 
            {
                icon: new CircleImageIcon({
                    iconUrl: '/cdp/' + element[0][0],
                })
            }).addTo(map);
        
        markers.push(marker);
        bindPopup(marker, element[0]);
    });
}

function remove_markers() {
    while (markers.length > 0) {
        markers[0].remove();
        markers.splice(0, 1);
    }

    polyline.remove();
}

function combine_markers(locations, map) {
    var managed = new Array(locations.length);
    managed.fill(0, 0, locations.length);

    var combined_markers = [];
    var waypoints = [];

    var location_to_manage = 0;

    var current_marker = [];
    var current_waypoint = [];
    
    current_waypoint = -1;
    while (locations.length > 0) {
        current_marker = new Array(0);
        current_waypoint++;

        if (managed[location_to_manage] != 0) {
            waypoints.push(managed[location_to_manage] - 1);
            locations.splice(0, 1);
            location_to_manage++;
            current_waypoint--;
            continue;
        } else {
            current_marker.push(locations[0]);

            locations.splice(0, 1);
            location_to_manage++;

            for (var i = 0; i < locations.length;) {
                var element = locations[i];

                if (managed[location_to_manage + i] != 0) {
                    i++;
                    continue;
                }

                if (in_range(current_marker[0][1], element[1], map)) {
                    current_marker.push(element);

                    if (i == 0) {
                        locations.splice(0, 1);
                        location_to_manage++;
                    } else {
                        managed[location_to_manage + i] = current_waypoint + 1;
                        i++; 
                    }
                } else {
                    i++;
                }
            }

            combined_markers.push(current_marker);
            waypoints.push(current_waypoint);
        }
    }

    return [combined_markers, waypoints];
}

function in_range(location1, location2, map) {
    return get_distance_in_px(location1, location2, map) < 25;
}

function get_distance_in_px(location1, location2, map) {
    var p1 = map.latLngToContainerPoint(L.latLng(location1[0], location1[1]));
    var p2 = map.latLngToContainerPoint(L.latLng(location2[0], location2[1]));

    var a = p1.x - p2.x;
    var b = p1.y - p2.y;

    return Math.sqrt(a * a + b * b);
}

function refactor_markers(combined_markers) {
    var m = [];

    combined_markers.forEach(element => {
        m.push([element.map(item => item[0]), median(element.map(item => item[1]))]);
    });

    return m;
}

function refactor_waypoints(waypoints, refactored_markers) {
    var w = [];

    waypoints.forEach(element => {
        w.push(refactored_markers[element][1]);
    });

    return w;
}

function get_distance_of_journey(waypoints) {
    var distance = 0.0;

    for (var i = 0; i < waypoints.length - 1; i++) {
        console.log(waypoints);
        distance += L.latLng(waypoints[i][0], waypoints[i][1]).distanceTo(L.latLng(waypoints[i + 1][0], waypoints[i + 1][1]));
    }

    return distance;
}

function median(locations) {
    var l = [0.0000, 0.0000];

    locations.forEach(element => {
        l[0] += element[0];
        l[1] += element[1];
    });

    return [l[0] / locations.length, l[1] / locations.length];
}

function bindPopup(marker, ids) {
    var popup = document.getElementById('popup');

    marker.on('click', function() {
        while (popup.firstChild) {
            popup.removeChild(popup.lastChild);
        }

        var image = document.createElement('img');
        image.setAttribute('id', 'current-popup-image');
        image.setAttribute('class', 'unselectable');
        image.setAttribute('src', '/cdp/' + ids[0]);
        popup.appendChild(image);

        popup.addEventListener('click', function(e) {
            if (e.target !== popup)
                return;

            popup.style.display = 'none';
        });

        popup.style.display = 'block';

        if (ids.length == 1)
            return;

        var next = document.createElement('a');
        next.setAttribute('id', 'next');
        next.setAttribute('class', 'unselectable');
        next.innerText = '❯';
        popup.appendChild(next);

        var prev = document.createElement('a');
        prev.setAttribute('id', 'prev');
        prev.setAttribute('class', 'unselectable');
        prev.innerText = '❮';
        popup.appendChild(prev);

        var current_image_id = 0;

        next.addEventListener('click', function() {
            current_image_id++;
            current_image_id = current_image_id % ids.length;

            image.setAttribute('src', '/cdp/' + ids[current_image_id]);
        });

        prev.addEventListener('click', function() {
            current_image_id--;
            
            if (current_image_id < 0)
                current_image_id = ids.length - 1;

            image.setAttribute('src', '/cdp/' + ids[current_image_id]);
        });
    });
}