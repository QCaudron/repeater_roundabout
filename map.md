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

L.marker([47.6171693850, -122.3181346817]).bindPopup('RR# 1 - WW7PSR (146.960)<br>RR# 2 - WW7PSR (52.870)<br>RR# 3 - WW7PSR (440.775)<br>RR# 39 - W7ACS (442.300)<br>RR# 40 - W7ACS (444.550)<br>RR# 41 - W7ACS (442.875)<br>').addTo(map);
L.marker([47.7622489900, -122.3494988000]).bindPopup('RR# 4 - W7AUX (442.825)<br>RR# 5 - W7AUX (440.300)<br>RR# 6 - W7AUX (224.020)<br>').addTo(map);
L.marker([47.4508018500, -122.2870025600]).bindPopup('RR# 7 - NC7G (146.660)<br>RR# 8 - WA7ST (443.100)<br>').addTo(map);
L.marker([48.0583000200, -122.6880035400]).bindPopup('RR# 9 - AA7MI (440.725)<br>').addTo(map);
L.marker([47.8566093400, -122.2836761500]).bindPopup('RR# 10 - W7FLY (443.925)<br>').addTo(map);
L.marker([47.6748100000, -122.0534360000]).bindPopup('RR# 11 - W7DX (147.000)<br>').addTo(map);
L.marker([47.6557998700, -122.5479965200]).bindPopup('RR# 12 - W7NPC (53.430)<br>RR# 13 - W7NPC (444.475)<br>RR# 14 - W7NPC (444.5625)<br>RR# 15 - W7NPC (1290.500)<br>').addTo(map);
L.marker([47.7724990800, -122.9300003100]).bindPopup('RR# 16 - K7DK (440.950)<br>').addTo(map);
L.marker([47.6884994500, -122.1559982300]).bindPopup('RR# 17 - K7LWH (145.490)<br>').addTo(map);
L.marker([47.5486984300, -122.7860031100]).bindPopup('RR# 18 - K7PP (441.200)<br>').addTo(map);
L.marker([47.5171508800, -122.0399971000]).bindPopup('RR# 19 - N9VW (53.830)<br>RR# 92 - N7KGJ (444.525)<br>').addTo(map);
L.marker([47.6321506500, -122.3549995450]).bindPopup('RR# 20 - WW7SEA (444.700)<br>RR# 21 - WW7SEA (444.425)<br>').addTo(map);
L.marker([47.5038986200, -121.9759979200]).bindPopup('RR# 22 - K7NWS (145.330)<br>RR# 23 - K7NWS (224.340)<br>RR# 24 - K7NWS (442.075)<br>').addTo(map);
L.marker([47.4883435700, -121.9467813000]).bindPopup('RR# 25 - K7LED (146.820)<br>RR# 26 - K7LED (224.120)<br>RR# 35 - WW7STR (146.875)<br>RR# 36 - WW7STR (443.050)<br>').addTo(map);
L.marker([46.8431010000, -122.3149560000]).bindPopup('RR# 27 - W7EAT (146.700)<br>RR# 29 - W7EAT (442.725)<br>').addTo(map);
L.marker([47.0531560000, -122.2948250000]).bindPopup('RR# 28 - W7EAT (224.180)<br>').addTo(map);
L.marker([47.2528991700, -122.4440002400]).bindPopup('RR# 30 - W7DK (147.280)<br>RR# 31 - W7DK (440.625)<br>').addTo(map);
L.marker([47.2787017800, -122.5120010400]).bindPopup('RR# 32 - W7DK (145.210)<br>').addTo(map);
L.marker([46.8429336533, -122.7643330900]).bindPopup('RR# 33 - W7DK (147.380)<br>RR# 99 - NT7H (224.460)<br>RR# 100 - NT7H (441.400)<br>').addTo(map);
L.marker([47.1998996700, -121.7554969750]).bindPopup('RR# 34 - W7AAO (145.370)<br>RR# 102 - W7SIX (53.870)<br>').addTo(map);
L.marker([47.5441978925, -122.1038913275]).bindPopup('RR# 37 - WW7STR (224.440)<br>RR# 38 - WW7STR (927.2125)<br>RR# 47 - W7RNK (147.995)<br>RR# 90 - KE7GFZ (441.825)<br>').addTo(map);
L.marker([47.6510101000, -122.3893988000]).bindPopup('RR# 42 - W7ACS (443.475)<br>').addTo(map);
L.marker([47.6901190000, -122.3177855000]).bindPopup('RR# 43 - W7ACS (443.650)<br>').addTo(map);
L.marker([47.7642647150, -122.2810041150]).bindPopup('RR# 44 - W7ACS (440.600)<br>RR# 111 - WA7FUS (224.220)<br>').addTo(map);
L.marker([47.5209999100, -122.3430023200]).bindPopup('RR# 45 - W7ACS (443.200)<br>RR# 61 - W7AW (440.975)<br>').addTo(map);
L.marker([48.1170005800, -122.7600021400]).bindPopup('RR# 46 - W7JCR (145.150)<br>').addTo(map);
L.marker([47.3768501300, -122.0529975900]).bindPopup('RR# 48 - KF7NPL (147.260)<br>RR# 49 - KF7NPL (442.675)<br>').addTo(map);
L.marker([46.9730987500, -123.1350021400]).bindPopup('RR# 50 - K7CPR (145.470)<br>RR# 101 - W7SIX (53.570)<br>RR# 103 - W7SIX (927.300)<br>').addTo(map);
L.marker([46.4879989600, -123.2144966150]).bindPopup('RR# 51 - K7PG (147.060)<br>RR# 113 - W7WRG (224.080)<br>').addTo(map);
L.marker([47.8089300000, -122.4928300000]).bindPopup('RR# 52 - NW7DR (147.4625)<br>').addTo(map);
L.marker([47.8439760000, -122.5427530000]).bindPopup('RR# 53 - NW7DR (444.725)<br>').addTo(map);
L.marker([47.2032012900, -122.2399978600]).bindPopup('RR# 54 - W7PSE (443.625)<br>').addTo(map);
L.marker([47.0329494500, -122.8990020750]).bindPopup('RR# 55 - W7PSE (145.150)<br>RR# 98 - NT7H (147.360)<br>').addTo(map);
L.marker([47.2792420000, -121.3487440000]).bindPopup('RR# 56 - W7PSE (442.725)<br>').addTo(map);
L.marker([47.2211990400, -121.8509979200]).bindPopup('RR# 57 - N7OEP (53.330)<br>RR# 58 - N7OEP (440.075)<br>').addTo(map);
L.marker([47.5404067300, -122.3781346750]).bindPopup('RR# 59 - W7AW (145.130)<br>RR# 60 - W7AW (441.800)<br>').addTo(map);
L.marker([48.1915016200, -122.5149993900]).bindPopup('RR# 62 - W7PIG (223.880)<br>').addTo(map);
L.marker([48.2249984700, -122.5000000000]).bindPopup('RR# 63 - W7PIG (147.360)<br>').addTo(map);
L.marker([47.9979496000, -122.1944999650]).bindPopup('RR# 64 - WA7LAW (147.180)<br>RR# 65 - WA7LAW (444.575)<br>').addTo(map);
L.marker([48.6777331000, -122.8316675800]).bindPopup('RR# 66 - K7SKW (146.740)<br>RR# 67 - K7SKW (444.050)<br>RR# 82 - N7JN (224.480)<br>').addTo(map);
L.marker([48.7821006800, -122.3700027500]).bindPopup('RR# 68 - K7SKW (443.750)<br>').addTo(map);
L.marker([48.8017997750, -122.4614982650]).bindPopup('RR# 69 - K7SKW (147.160)<br>RR# 70 - K7SKW (443.650)<br>').addTo(map);
L.marker([48.5889015200, -122.1525001500]).bindPopup('RR# 71 - N7GDE (145.190)<br>RR# 110 - N7RIG (224.780)<br>').addTo(map);
L.marker([47.8121999800, -122.3248012200]).bindPopup('RR# 72 - WA7DEM (146.780)<br>RR# 78 - WA7DEM (444.025)<br>').addTo(map);
L.marker([48.0517997700, -122.1770019500]).bindPopup('RR# 73 - WA7DEM (224.380)<br>').addTo(map);
L.marker([47.9128990200, -122.0979995700]).bindPopup('RR# 74 - WA7DEM (442.975)<br>').addTo(map);
L.marker([47.7882003800, -122.3089981100]).bindPopup('RR# 75 - WA7DEM (443.725)<br>').addTo(map);
L.marker([48.1369500000, -121.9814000000]).bindPopup('RR# 76 - WA7DEM (146.92)<br>').addTo(map);
L.marker([47.9585000000, -122.3750000000]).bindPopup('RR# 77 - WA7DEM (440.375)<br>').addTo(map);
L.marker([48.2494400000, -121.5694900000]).bindPopup('RR# 79 - WA7DEM (444.300)<br>').addTo(map);
L.marker([47.7376770000, -122.2307900000]).bindPopup('RR# 80 - NE7MC (442.000)<br>').addTo(map);
L.marker([48.5603981000, -123.1200027500]).bindPopup('RR# 81 - N7JN (146.700)<br>').addTo(map);
L.marker([48.5343017600, -123.0169982900]).bindPopup('RR# 83 - N7JN (145.250)<br>RR# 84 - N7JN (442.4625)<br>').addTo(map);
L.marker([47.3223495500, -122.3125019075]).bindPopup('RR# 85 - WA7FW (147.040)<br>RR# 86 - WA7FW (146.760)<br>RR# 87 - WA7FW (442.950)<br>RR# 88 - WA7FW (146.840)<br>').addTo(map);
L.marker([47.3507995600, -122.3229980500]).bindPopup('RR# 89 - WA7FW (443.850)<br>').addTo(map);
L.marker([47.6299300000, -121.9500800000]).bindPopup('RR# 91 - WA7TBP (223.960)<br>').addTo(map);
L.marker([47.5404014600, -122.6360015900]).bindPopup('RR# 93 - N7IG (145.390)<br>').addTo(map);
L.marker([47.6445007300, -122.6949996900]).bindPopup('RR# 94 - KC7Z (444.075)<br>').addTo(map);
L.marker([47.2150993300, -123.1009979200]).bindPopup('RR# 95 - N7SK (146.720)<br>RR# 96 - N7SK (443.250)<br>RR# 97 - N7SK (927.4125)<br>').addTo(map);
L.marker([47.3866150000, -122.8609950000]).bindPopup('RR# 104 - NM7E (145.170)<br>').addTo(map);
L.marker([48.2125015300, -122.7050018300]).bindPopup('RR# 105 - W7AVM (146.860)<br>').addTo(map);
L.marker([48.0982722000, -122.5731977000]).bindPopup('RR# 106 - N7KN (441.425)<br>').addTo(map);
L.marker([46.9793700000, -122.4399700000]).bindPopup('RR# 107 - WA7ROY (444.175)<br>').addTo(map);
L.marker([47.5683670000, -122.2207290000]).bindPopup('RR# 108 - W7MIR (147.160)<br>RR# 109 - W7MIR (440.150)<br>').addTo(map);
L.marker([47.2040600000, -121.7956880000]).bindPopup('RR# 112 - W7WRG (224.880)<br>').addTo(map);

</script>
