// Javascript file for my website

// Model
var locations = [
      {title: "China Town", location: {lat: 38.931447, lng: -77.038175}, category: "Restaurant", selected: 0, PlaceID: "ChIJm-uSRCHIt4kR_FFrlMV9WEk"},
      {title: "Beau Thai", location: {lat: 38.930303, lng: -77.038255}, category: "Restaurant", selected: 0, PlaceID: "ChIJR3mNPCHIt4kRg7lh0btyMNA"},
      {title: "Argyle", location: {lat: 38.932446, lng: -77.039006}, category: "Grocery", selected: 0, PlaceID: "ChIJATuAVSHIt4kR1lhRSKwzMOQ"},
      {title: "Mt. Pleasant Neighborhood Library", location: {lat: 38.9305275, lng: -77.0372412}, category: "Entertainment", selected: 0, PlaceID: "ChIJ0fIsJSHIt4kR34nU2Q4E3UM"},
      {title: "Suns Cinema", location: {lat: 38.9289535, lng: -77.0372414}, category: "Bar", selected: 0, PlaceID: "ChIJQcMN5SDIt4kRZZq8cQVIjU0"},
      {title: "Best World", location: {lat: 38.9310368, lng: -77.03833259999999}, category: "Grocery", selected: 0, PlaceID: "ChIJ80jrNyHIt4kRf9zX1J6dKKg"},
      {title: "Elle", location: {lat: 38.931912, lng: -77.038392}, category: "Bar", selected: 0, PlaceID: "ChIJlfHBWyHIt4kROJ7C5CD7Kr4"}
];


// Blank map variable
var map;

// Create a new blank array for all the listing markers.
var markers = [];


/// Get Wikipedia Article on Mount Pleasant
function loadData() {
    var $wikiHead = $("#wikipedia-header");
    var $wikiElem = $("#wikipedia-links");

    // clear out old data before new request
    $wikiElem.text("");

    // load wikipedia data
    var wikiUrl = "http://en.wikipedia.org/w/api.php?action=opensearch&search=" + "Mount_Pleasant,_Washington,_D.C." + "&format=json&callback=wikiCallback";
    var wikiRequestTimeout = setTimeout(function(){
        $wikiElem.text("failed to get wikipedia resources");
    }, 8000);

    $.ajax({
        url: wikiUrl,
        dataType: "jsonp",
        jsonp: "callback",
        success: function( response ) {
            var articleList = response[1];
            var description = response[2];
            for (var i = 0; i < articleList.length; i++) {
                articleStr = articleList[i];
                var url = "http://en.wikipedia.org/wiki/" + articleStr;
                $wikiHead.append("<h6>" + description + "</h6>");
                $wikiElem.append('<li><a href="' + url + '" + target="_blank">' + articleStr + '</a></li>');
            };

            clearTimeout(wikiRequestTimeout);
        }
    });

    return false;
};

initMap = function() {
    var viewModel = function() {
        var self = this;

        // Create a styles array to use with the map.
        // Constructor creates a new map - only center and zoom are required.
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 38.929717, lng: -77.035554},
          zoom: 16,
          mapTypeControl: false
        });

        // These are the real estate listings that will be shown to the user.
        // Normally we'd have these in a database instead.

        // Create the infowindow for each marker
        var largeInfowindow = new google.maps.InfoWindow();

        // Get information about each marker
        var service = new google.maps.places.PlacesService(map);

        // Style the markers a bit. This will be our listing marker icon.
        var defaultIcon = makeMarkerIcon('B42020');

        // Create a "highlighted location" marker color for when the user
        // mouses over the marker.
        var highlightedIcon = makeMarkerIcon('FFFF24');

        // The following group uses the location array to create an array of markers on initialize.
        for (var i = 0; i < locations.length; i++) {
            // Get the position from the location array.
            var position = locations[i].location;
            var title = locations[i].title;
            var placeID = locations[i].PlaceID;
            // Create a marker per location, and put into markers array.
            var marker = new google.maps.Marker({
                position: position,
                title: title,
                animation: google.maps.Animation.DROP,
                icon: defaultIcon,
                id: i,
                placeID: placeID
                });

            // Push the marker to our array of markers.
            markers.push(marker);

            // Create an onclick event to open the large infowindow at each marker.
            marker.addListener('click', function() {
                self.markerSelect(this);
                self.populateInfoWindow(this, largeInfowindow);
                self.openInfoWindow(this, largeInfowindow);
                self.bounce();
            });

            // Two event listeners - one for mouseover, one for mouseout,
            // to change the colors back and forth.
            marker.addListener('mouseover', function() {
                this.setIcon(highlightedIcon);
            });
            marker.addListener('mouseout', function() {
                this.setIcon(defaultIcon);
            });
        };

        self.bounce = function() {
            //var b = locations.map(function(e) { return e.title; }).indexOf(marker.title);
            for (var i = 0; i < locations.length; i++) {
                if (locations[i].selected===0){
                    markers[i].setAnimation(null);
                } else {
                    markers[i].setAnimation(google.maps.Animation.BOUNCE);
                }
            }
        };

        // This function populates the infowindow when the marker is clicked. We'll only allow
        // one infowindow which will open at the marker that is clicked, and populate based
        // on that markers position.
        self.populateInfoWindow = function(marker, infowindow) {
            // Check to make sure the infowindow is not already opened on this marker.
            if (infowindow.marker != marker) {
                infowindow.marker = marker;
                infowindow.setContent('');
                service.getDetails({
                    placeId: marker.placeID
                }, function(place, status) {
                    if (status === google.maps.places.PlacesServiceStatus.OK) {
                        var c = place.rating;
                        var d = place.reviews;
                    }
                infowindow.setContent('<div style="font-weight:bold;">' + marker.title + '</div>' + 'Average Rating: ' + c + ' Stars' + '<br>Review: ' + d[0].text + '<br>-' + d[0].author_name);
                });
                // Make sure the marker property is cleared if the infowindow is closed.
                infowindow.addListener('closeclick', function() {
                    infowindow.marker = null;
                });
            }
        };

        //Open the infowindow
        self.openInfoWindow = function(marker, infowindow){
            // Close all markers
            for (var i = 0; i < markers.length; i++) {
                infowindow.close(map, marker[i]);        
            }
            //Open the infowindow if the marker is for a newly selected location, close it if you are deselecting a location
            var b = locations.map(function(e) { return e.title; }).indexOf(marker.title);
            if (locations[b].selected===0){
                infowindow.close(map, marker);
            } else {
                infowindow.open(map, marker);
            }
        };

        // Identify the the location as selected if the marker for the location is clicked
        self.markerSelect = function(marker) {
            var b = locations.map(function(e) { return e.title; }).indexOf(marker.title);
            if (locations[b].selected===1){
                locations[b].selected=0;
            } else {
                for (var i = 0; i < locations.length; i++) {
                    locations[i].selected=0;
                }
                locations[b].selected=1;
            }
        };

        //Show the listings
        for (var i = 0; i < markers.length; i++) {
                    markers[i].setMap(map);
        }

        // This function takes in a COLOR, and then creates a new marker
        // icon of that color. The icon will be 21 px wide by 34 high, have an origin
        // of 0, 0 and be anchored at 10, 34).
        function makeMarkerIcon(markerColor) {
            var markerImage = new google.maps.MarkerImage('http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|'+ markerColor + '|40|_|%E2%80%A2',
            new google.maps.Size(21, 34),
            new google.maps.Point(0, 0),
            new google.maps.Point(10, 34),
            new google.maps.Size(21,34));
            return markerImage;
            }


        // Knockout code for the ViewModel
        self.containsObject= function(obj, list) {
            var i;
            for (i = 0; i < list.length; i++) {
                if (list[i].title === obj) {
                return true;
                }
            }
            return false;
        }

        self.places = ko.observableArray([]);
        self.categories = ko.observableArray([]);

        locations.forEach(function(locationItem){
            self.categories.push(locationItem.category);
        });

        self.categories.push('All');

        self.categories = ko.dependentObservable(function() {
            return ko.utils.arrayGetDistinctValues(self.categories()).sort();
        }, viewModel);

        locations.forEach(function(locationItem){
            self.places.push({title: locationItem.title});
        });

        var id;
        self.selectLocation = function(item, event) {
            markers.forEach(function(thing){
                if(thing.title===item.title){
                    id = thing.id;
                    if(locations[thing.id].selected===1) {
                        locations[thing.id].selected = 0;
                    } else {
                        locations[thing.id].selected = 1;
                    }
                } else {
                    locations[thing.id].selected = 0;
                }
            });
            self.populateInfoWindow(markers[id], largeInfowindow);
            self.openInfoWindow(markers[id], largeInfowindow);
            self.bounce();
        };

        self.x = ko.observable();
        self.selectCategory = function() {
            self.places([]);
            if (self.x() != 'All') {
                locations.forEach(function(locationItem){
                    if (locationItem.category == self.x()) {
                        self.places.push(locationItem);
                    }
                })
                markers.forEach(function(thing){
                    if(self.containsObject(thing.title, self.places())){
                        thing.setMap(map);
                    } else {
                        thing.setMap(null);
                    }
                });
            } else {
                    locations.forEach(function(locationItem){
                        self.places.push({title: locationItem.title});
                        })
                    markers.forEach(function(thing1){
                        thing1.setMap(map);
                    })
                }
        }
    };

    ko.applyBindings(new viewModel());

};

loadData();