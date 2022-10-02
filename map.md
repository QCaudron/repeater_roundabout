---
title: Repeater Map
subtitle: Some location magic.
head-extra: leaflet.html
---

<div id="map" style="height: 300px;"></div>

<script>
var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

L.marker([51.5, -0.09]).bindPopup("I am a circle.").addTo(map);
</script>
