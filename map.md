---
title: Repeater Map
subtitle: Some location magic.
head-extra: leaflet.html
---

The locations for these repeaters are approximate, and sourced from RepeaterBook.

<div id="map" style="height: 730px; border-radius: 500px;"></div>

<script>
var map = L.map('map').setView([47.67, -122.4], 8);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

L.marker([47.6153311086, -122.3198299886]).bindPopup('RR# 1 - WW7PSR (146.960)<br>RR# 2 - WW7PSR (52.870)<br>RR# 3 - WW7PSR (440.775)<br>RR# 7 - W7ACS (442.300)<br>RR# 8 - W7ACS (444.550)<br>RR# 9 - W7ACS (442.875)<br>RR# 27 - WW7SEA (444.550)<br>').addTo(map);
L.marker([47.4508018500, -122.2870025600]).bindPopup('RR# 4 - NC7G (146.660)<br>RR# 5 - WA7ST (443.100)<br>').addTo(map);
L.marker([48.5833015400, -122.1449966400]).bindPopup('RR# 6 - N7GDE (145.190)<br>').addTo(map);
L.marker([47.6510101000, -122.3893988000]).bindPopup('RR# 10 - W7ACS (443.475)<br>').addTo(map);
L.marker([47.6901190000, -122.3177855000]).bindPopup('RR# 11 - W7ACS (443.650)<br>').addTo(map);
L.marker([47.7719300000, -122.2810100000]).bindPopup('RR# 12 - W7ACS (440.600)<br>').addTo(map);
L.marker([47.5209999100, -122.3430023200]).bindPopup('RR# 13 - W7ACS (443.200)<br>').addTo(map);
L.marker([47.6299300000, -121.9500800000]).bindPopup('RR# 14 - WA7TBP (223.960)<br>').addTo(map);
L.marker([48.1170005800, -122.7600021400]).bindPopup('RR# 15 - W7JCR (145.150)<br>').addTo(map);
L.marker([48.0583000200, -122.6880035400]).bindPopup('RR# 16 - AA7MI (440.725)<br>').addTo(map);
L.marker([47.0279998800, -122.8970031700]).bindPopup('RR# 17 - NT7H (147.360)<br>').addTo(map);
L.marker([46.8428497300, -122.7649993900]).bindPopup('RR# 18 - NT7H (224.460)<br>RR# 19 - NT7H (441.400)<br>').addTo(map);
L.marker([47.5683670000, -122.2207290000]).bindPopup('RR# 20 - W7MIR (147.160)<br>RR# 21 - W7MIR (440.150)<br>').addTo(map);
L.marker([47.6445007300, -122.6949996900]).bindPopup('RR# 22 - KC7Z (444.075)<br>').addTo(map);
L.marker([48.2125015300, -122.7050018300]).bindPopup('RR# 23 - W7AVM (146.860)<br>').addTo(map);
L.marker([48.0982722000, -122.5731977000]).bindPopup('RR# 24 - N7KN (441.425)<br>').addTo(map);
L.marker([47.7724990800, -122.9300003100]).bindPopup('RR# 25 - K7DK (440.950)<br>').addTo(map);
L.marker([47.6321506500, -122.3549995450]).bindPopup('RR# 26 - WW7SEA (444.700)<br>RR# 28 - WW7SEA (444.425)<br>').addTo(map);
L.marker([47.7622489900, -122.3494988000]).bindPopup('RR# 29 - W7AUX (442.825)<br>RR# 30 - W7AUX (440.300)<br>RR# 31 - W7AUX (224.020)<br>').addTo(map);
L.marker([47.5038986200, -121.9759979200]).bindPopup('RR# 32 - K7NWS (145.330)<br>RR# 33 - K7NWS (224.340)<br>RR# 34 - K7NWS (442.075)<br>').addTo(map);
L.marker([47.6884994500, -122.1559982300]).bindPopup('RR# 35 - K7LWH (53.170)<br>RR# 36 - K7LWH (145.490)<br>').addTo(map);
L.marker([47.6814994800, -122.2089996300]).bindPopup('RR# 37 - K7LWH (224.360)<br>RR# 38 - K7LWH (441.075)<br>').addTo(map);
L.marker([47.8566093400, -122.2836761500]).bindPopup('RR# 39 - W7FLY (443.925)<br>').addTo(map);

</script>
