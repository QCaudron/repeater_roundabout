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

L.marker([47.6171693850, -122.3181346817]).bindPopup('WW7PSR 146.960<br>WW7PSR 52.870<br>WW7PSR 440.775<br>W7ACS 442.300<br>W7ACS 444.550<br>W7ACS 442.875<br>').addTo(map);
L.marker([47.7622489900, -122.3494988000]).bindPopup('W7AUX 442.825<br>W7AUX 440.300<br>W7AUX 224.020<br>').addTo(map);
L.marker([47.4508018500, -122.2870025600]).bindPopup('NC7G 146.660<br>WA7ST 443.100<br>').addTo(map);
L.marker([48.0583000200, -122.6880035400]).bindPopup('AA7MI 440.725<br>').addTo(map);
L.marker([47.8566093400, -122.2836761500]).bindPopup('W7FLY 443.925<br>').addTo(map);
L.marker([47.6748100000, -122.0534360000]).bindPopup('W7DX 147.000<br>').addTo(map);
L.marker([47.6557998700, -122.5479965200]).bindPopup('W7NPC 53.430<br>W7NPC 444.475<br>W7NPC 444.5625<br>W7NPC 1290.500<br>').addTo(map);
L.marker([47.7724990800, -122.9300003100]).bindPopup('K7DK 440.950<br>').addTo(map);
L.marker([47.6884994500, -122.1559982300]).bindPopup('K7LWH 145.490<br>').addTo(map);
L.marker([47.5486984300, -122.7860031100]).bindPopup('K7PP 441.200<br>').addTo(map);
L.marker([47.5171508800, -122.0399971000]).bindPopup('N9VW 53.830<br>N7KGJ 444.525<br>').addTo(map);
L.marker([47.6321506500, -122.3549995450]).bindPopup('WW7SEA 444.700<br>WW7SEA 444.425<br>').addTo(map);
L.marker([47.5038986200, -121.9759979200]).bindPopup('K7NWS 145.330<br>K7NWS 224.340<br>K7NWS 442.075<br>').addTo(map);
L.marker([47.4883435700, -121.9467813000]).bindPopup('K7LED 146.820<br>K7LED 224.120<br>WW7STR 146.875<br>WW7STR 443.050<br>').addTo(map);
L.marker([46.8431010000, -122.3149560000]).bindPopup('W7EAT 146.700<br>W7EAT 442.725<br>').addTo(map);
L.marker([47.0531560000, -122.2948250000]).bindPopup('W7EAT 224.180<br>').addTo(map);
L.marker([47.2528991700, -122.4440002400]).bindPopup('W7DK 147.280<br>W7DK 440.625<br>').addTo(map);
L.marker([47.2787017800, -122.5120010400]).bindPopup('W7DK 145.210<br>').addTo(map);
L.marker([46.8431015000, -122.7630004900]).bindPopup('W7DK 147.380<br>').addTo(map);
L.marker([47.1997985800, -121.7559967000]).bindPopup('W7AAO 145.370<br>').addTo(map);
L.marker([47.5441978925, -122.1038913275]).bindPopup('WW7STR 224.440<br>WW7STR 927.2125<br>W7RNK 147.995<br>KE7GFZ 441.825<br>').addTo(map);
L.marker([47.6510101000, -122.3893988000]).bindPopup('W7ACS 443.475<br>').addTo(map);
L.marker([47.6901190000, -122.3177855000]).bindPopup('W7ACS 443.650<br>').addTo(map);
L.marker([47.7719300000, -122.2810100000]).bindPopup('W7ACS 440.600<br>').addTo(map);
L.marker([47.5209999100, -122.3430023200]).bindPopup('W7ACS 443.200<br>W7AW 440.975<br>').addTo(map);
L.marker([48.1170005800, -122.7600021400]).bindPopup('W7JCR 145.150<br>').addTo(map);
L.marker([47.3768501300, -122.0529975900]).bindPopup('KF7NPL 147.260<br>KF7NPL 442.675<br>').addTo(map);
L.marker([46.9730987500, -123.1350021400]).bindPopup('K7CPR 145.470<br>').addTo(map);
L.marker([46.4880981400, -123.2149963400]).bindPopup('K7PG 147.060<br>').addTo(map);
L.marker([46.6619987500, -122.9639968900]).bindPopup('K7PG 145.430<br>').addTo(map);
L.marker([47.8089300000, -122.4928300000]).bindPopup('NW7DR 147.4625<br>').addTo(map);
L.marker([47.8439760000, -122.5427530000]).bindPopup('NW7DR 444.725<br>').addTo(map);
L.marker([47.2032012900, -122.2399978600]).bindPopup('W7PSE 443.625<br>').addTo(map);
L.marker([47.0378990200, -122.9010009800]).bindPopup('W7PSE 145.150<br>').addTo(map);
L.marker([47.2792420000, -121.3487440000]).bindPopup('W7PSE 442.725<br>').addTo(map);
L.marker([47.2211990400, -121.8509979200]).bindPopup('N7OEP 53.330<br>N7OEP 440.075<br>').addTo(map);
L.marker([47.5404067300, -122.3781346750]).bindPopup('W7AW 145.130<br>W7AW 441.800<br>').addTo(map);
L.marker([48.1915016200, -122.5149993900]).bindPopup('W7PIG 223.880<br>').addTo(map);
L.marker([48.2249984700, -122.5000000000]).bindPopup('W7PIG 147.360<br>').addTo(map);
L.marker([47.9979496000, -122.1944999650]).bindPopup('WA7LAW 147.180<br>WA7LAW 444.575<br>').addTo(map);
L.marker([48.6777331000, -122.8316675800]).bindPopup('K7SKW 146.740<br>K7SKW 444.050<br>N7JN 224.480<br>').addTo(map);
L.marker([48.7821006800, -122.3700027500]).bindPopup('K7SKW 443.750<br>').addTo(map);
L.marker([48.8017997750, -122.4614982650]).bindPopup('K7SKW 147.160<br>K7SKW 443.650<br>').addTo(map);
L.marker([48.5833015400, -122.1449966400]).bindPopup('N7GDE 145.190<br>').addTo(map);
L.marker([47.8121999800, -122.3248012200]).bindPopup('WA7DEM 146.780<br>WA7DEM 444.025<br>').addTo(map);
L.marker([48.0517997700, -122.1770019500]).bindPopup('WA7DEM 224.380<br>').addTo(map);
L.marker([47.9128990200, -122.0979995700]).bindPopup('WA7DEM 442.975<br>').addTo(map);
L.marker([47.7882003800, -122.3089981100]).bindPopup('WA7DEM 443.725<br>').addTo(map);
L.marker([48.1369500000, -121.9814000000]).bindPopup('WA7DEM 146.92<br>').addTo(map);
L.marker([47.9585000000, -122.3750000000]).bindPopup('WA7DEM 440.375<br>').addTo(map);
L.marker([48.2494400000, -121.5694900000]).bindPopup('WA7DEM 444.300<br>').addTo(map);
L.marker([47.7376770000, -122.2307900000]).bindPopup('NE7MC 442.000<br>').addTo(map);
L.marker([48.5603981000, -123.1200027500]).bindPopup('N7JN 146.700<br>').addTo(map);
L.marker([48.5343017600, -123.0169982900]).bindPopup('N7JN 145.250<br>N7JN 442.4625<br>').addTo(map);
L.marker([47.3223495500, -122.3125019075]).bindPopup('WA7FW 147.040<br>WA7FW 146.760<br>WA7FW 442.950<br>WA7FW 146.840<br>').addTo(map);
L.marker([47.3507995600, -122.3229980500]).bindPopup('WA7FW 443.850<br>').addTo(map);
L.marker([47.6299300000, -121.9500800000]).bindPopup('WA7TBP 223.960<br>').addTo(map);
L.marker([47.5404014600, -122.6360015900]).bindPopup('N7IG 145.390<br>').addTo(map);

</script>
