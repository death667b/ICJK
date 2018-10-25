var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -26, lng: 134.644},
    zoom: 5
    });
}

geocode('brisbane');    

function geocode(location){
var location ;
axios.get('https://maps.googleapis.com/maps/api/geocode/json',{
    params:{
        address:location,
        key:'AIzaSyChkL1-v3Cgf3zc1BfNFucXnovUyZsRiBQ'
     }
    })
    .then(function(response){
    // Log full response
    console.log(response.data.results[0]);  
    // Geometry
    var lat = response.data.results[0].geometry.location.lat;
    var lng = response.data.results[0].geometry.location.lng;
    console.log(lat,lng);
    })
    .catch(function(error){
    console.log(error);
    });
}  