---
title: Repeater Map
subtitle: Some location magic.
head-extra: leaflet.html
---

The locations for these repeaters are sourced from RepeaterBook. If any are incorrect, please contact [Quentin K7DRQ](mailto:k7drq@psrg.org) to have them updated on this map; please also update the repeater's information on RepeaterBook.

<div id="map" style="height: 800px;"></div>

<script>
var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

L.marker([47.62400055, -122.31500244]).bindPopup("WW7PSR 52.870, 146.960, 440.775").addTo(map);

L.marker([47.76779938, -122.35299683]).bindPopup("W7AUX 442.825").addTo(map);
L.marker([47.75669861, -122.34600067]).bindPopup("W7AUX 224.020, 440.300").addTo(map);

L.marker([47.45080185, -122.28700256]).bindPopup("NC7G 146.660, WA7ST 443.100").addTo(map);

L.marker([47.85660934, -122.28367615]).bindPopup("W7FLY 443.925").addTo(map);

L.marker([47.67481000, -122.05343600]).bindPopup("W7DX 147.000").addTo(map);

L.marker([47.65579987, -122.54799652]).bindPopup("W7NPC 53.430, 444.475, 444.562, 1290.500").addTo(map);

L.marker([47.45109940, -122.55400085]).bindPopup("K7DK 440.950").addTo(map);

L.marker([47.68849945, -122.15599823]).bindPopup("K7LWH 145.490").addTo(map);
</script>
