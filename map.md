---
title: Repeater Map
subtitle: Some location magic.
head-extra: leaflet.html
---

The locations for these repeaters are approximate, and sourced from RepeaterBook.

<div id="map" style="height: 730px; border-radius: 500px;"></div>

<script>
var map = L.map('map').setView([47.54, -122.4], 8);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

L.marker([47.6171693850, -122.3181346817]).bindPopup('WW7PSR 146.960<br>WW7PSR 52.870<br>WW7PSR 440.775<br>W7ACS 442.300<br>W7ACS 444.550<br>W7ACS 442.875<br>').addTo(map);
L.marker([47.7622489900, -122.3494988000]).bindPopup('W7AUX 442.825<br>W7AUX 440.300<br>W7AUX 224.020<br>').addTo(map);
L.marker([47.4508018500, -122.2870025600]).bindPopup('NC7G 146.660<br>WA7ST 443.100<br>').addTo(map);
L.marker([48.0583000200, -122.6880035400]).bindPopup('AA7MI 440.725<br>').addTo(map);
L.marker([47.8566093400, -122.2836761500]).bindPopup('W7FLY 443.925<br>').addTo(map);
L.marker([47.6748100000, -122.0534360000]).bindPopup('W7DX 147.000<br>').addTo(map);
L.marker([47.6557998700, -122.5479965200]).bindPopup('W7NPC 444.475<br>W7NPC 53.430<br>W7NPC 444.5625<br>W7NPC 1290.500<br>').addTo(map);
L.marker([47.7724990800, -122.9300003100]).bindPopup('K7DK 440.950<br>').addTo(map);
L.marker([47.6884994500, -122.1559982300]).bindPopup('K7LWH 145.490<br>').addTo(map);
L.marker([47.5486984300, -122.7860031100]).bindPopup('K7PP 441.200<br>').addTo(map);
L.marker([47.5301017800, -122.0329971300]).bindPopup('N9VW 53.830<br>').addTo(map);
L.marker([47.6321506500, -122.3549995450]).bindPopup('WW7SEA 444.700<br>WW7SEA 444.425<br>').addTo(map);
L.marker([47.5038986200, -121.9759979200]).bindPopup('K7NWS 145.330<br>K7NWS 224.340<br>K7NWS 442.075<br>').addTo(map);
L.marker([47.4883435700, -121.9467813000]).bindPopup('K7LED 146.820<br>K7LED 224.120<br>WW7STR 146.875<br>WW7STR 443.050<br>').addTo(map);
L.marker([46.8431010000, -122.3149560000]).bindPopup('W7EAT 146.700<br>W7EAT 442.725<br>').addTo(map);
L.marker([47.0531560000, -122.2948250000]).bindPopup('W7EAT 224.180<br>').addTo(map);
L.marker([47.2528991700, -122.4440002400]).bindPopup('W7DK 147.280<br>W7DK 440.625<br>').addTo(map);
L.marker([47.2787017800, -122.5120010400]).bindPopup('W7DK 145.210<br>').addTo(map);
L.marker([46.8431015000, -122.7630004900]).bindPopup('W7DK 147.380<br>').addTo(map);
L.marker([47.1997985800, -121.7559967000]).bindPopup('W7AAO 145.370<br>').addTo(map);
L.marker([47.5402970000, -122.0998560000]).bindPopup('WW7STR 224.440<br>WW7STR 927.2125<br>W7RNK 147.995<br>').addTo(map);
L.marker([47.6510101000, -122.3893988000]).bindPopup('W7ACS 443.475<br>').addTo(map);
L.marker([47.6901190000, -122.3177855000]).bindPopup('W7ACS 443.650<br>').addTo(map);
L.marker([47.7719300000, -122.2810100000]).bindPopup('W7ACS 440.600<br>').addTo(map);
L.marker([47.5209999100, -122.3430023200]).bindPopup('W7ACS 443.200<br>').addTo(map);
L.marker([48.1170005800, -122.7600021400]).bindPopup('W7JCR 145.150<br>').addTo(map);

</script>
