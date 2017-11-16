//init Map
function initMap(){
	var options = {
	  zoom : 3,
	  center: {lat:23.903687,lng:121.079370}
}

//New Map
var map = new google.maps.Map(document.getElementById('map'),options);

//Add point marker
function addMarker(coords){
  var marker = new google.maps.Marker({
    position : coords,
    map: map
  });
}

//Use JQuery Read map.json
//Call addMarker Function to add point
var point = $.getJSON("{% static "json/map.json" %}" ,function(data){
  console.log("json file loading success!");
  for(var i=0;i<10;i++){
    addMarker(data[i]);
  }
});

}
