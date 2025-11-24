// mapa.js
// Muestra un mapa de Google Maps en la sección de contacto
// Reemplaza 'TU_API_KEY' por una API Key válida si quieres mapa real
function initMap() {
  var club = {lat: -34.6037, lng: -58.3816};
  var map = new google.maps.Map(document.getElementById('mapa'), {
    zoom: 15,
    center: club
  });
  var marker = new google.maps.Marker({position: club, map: map});
}
// El script de Google Maps debe llamarse con callback=initMap
