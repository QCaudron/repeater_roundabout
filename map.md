---
title: Repeater Map
subtitle: Some location magic.
head-extra: leaflet.html
---

The locations for these repeaters are approximate, and sourced from RepeaterBook.

<div id="map" style="height: 730px; border-radius: 500px;"></div>

<style>
    .custom-icon {
        background-color: #165a0a;
        border-radius: 50%;
        text-align: center;
        color: white;
    }

    .icon-label {
        line-height: 25px;
        /* Match the height of the icon */
    }
</style>


<script>
var map = L.map('map').setView([47.63, -122.75], 8);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

L.marker([47.6239004150, -122.3150024400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 1 - WW7PSR (146.960)<br>RR# 2 - WW7PSR (52.870)<br>RR# 3 - WW7PSR (440.775)<br>RR# 10 - W7ACS (442.875)<br>').addTo(map);
L.marker([47.4508018500, -122.2870025600], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 4 - NC7G (146.660)<br>RR# 5 - WA7ST (443.100)<br>').addTo(map);
L.marker([47.7724990800, -122.9300003100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>6</div>", iconSize: [25, 25]}) }).bindPopup('RR# 6 - K7DK (440.950)<br>').addTo(map);
L.marker([48.5833015400, -122.1449966400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>7</div>", iconSize: [25, 25]}) }).bindPopup('RR# 7 - N7GDE (145.190)<br>').addTo(map);
L.marker([47.6031132000, -122.3187965000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>8</div>", iconSize: [25, 25]}) }).bindPopup('RR# 8 - W7ACS (442.300)<br>').addTo(map);
L.marker([47.6043014500, -122.3300018300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>9</div>", iconSize: [25, 25]}) }).bindPopup('RR# 9 - W7ACS (444.550)<br>').addTo(map);
L.marker([47.6510101000, -122.3893988000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>11</div>", iconSize: [25, 25]}) }).bindPopup('RR# 11 - W7ACS (443.475)<br>').addTo(map);
L.marker([47.6901190000, -122.3177855000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>12</div>", iconSize: [25, 25]}) }).bindPopup('RR# 12 - W7ACS (443.650)<br>').addTo(map);
L.marker([47.7719300000, -122.2810100000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>13</div>", iconSize: [25, 25]}) }).bindPopup('RR# 13 - W7ACS (440.600)<br>').addTo(map);
L.marker([47.5209999100, -122.3430023200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>14</div>", iconSize: [25, 25]}) }).bindPopup('RR# 14 - W7ACS (443.200)<br>').addTo(map);
L.marker([47.6299300000, -121.9500800000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>15</div>", iconSize: [25, 25]}) }).bindPopup('RR# 15 - WA7TBP (223.960)<br>').addTo(map);
L.marker([48.1170005800, -122.7600021400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>16</div>", iconSize: [25, 25]}) }).bindPopup('RR# 16 - W7JCR (145.150)<br>').addTo(map);
L.marker([48.0583000200, -122.6880035400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>17</div>", iconSize: [25, 25]}) }).bindPopup('RR# 17 - AA7MI (440.725)<br>').addTo(map);
L.marker([47.0279998800, -122.8970031700], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>18</div>", iconSize: [25, 25]}) }).bindPopup('RR# 18 - NT7H (147.360)<br>').addTo(map);
L.marker([46.8429336533, -122.7643330900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 19 - NT7H (224.460)<br>RR# 20 - NT7H (441.400)<br>RR# 87 - W7DK (147.380)<br>').addTo(map);
L.marker([47.5683670000, -122.2207290000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 21 - W7MIR (147.160)<br>RR# 22 - W7MIR (440.150)<br>').addTo(map);
L.marker([47.6445007300, -122.6949996900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>23</div>", iconSize: [25, 25]}) }).bindPopup('RR# 23 - KC7Z (444.075)<br>').addTo(map);
L.marker([48.2125015300, -122.7050018300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>24</div>", iconSize: [25, 25]}) }).bindPopup('RR# 24 - W7AVM (146.860)<br>').addTo(map);
L.marker([48.0982722000, -122.5731977000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>25</div>", iconSize: [25, 25]}) }).bindPopup('RR# 25 - N7KN (441.425)<br>').addTo(map);
L.marker([47.6324996900, -122.3560028100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>26</div>", iconSize: [25, 25]}) }).bindPopup('RR# 26 - WW7SEA (444.700)<br>').addTo(map);
L.marker([47.7622489900, -122.3494988000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 27 - W7AUX (442.825)<br>RR# 28 - W7AUX (440.300)<br>RR# 29 - W7AUX (224.020)<br>').addTo(map);
L.marker([47.5038986200, -121.9759979200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 30 - K7NWS (145.330)<br>RR# 31 - K7NWS (224.340)<br>RR# 32 - K7NWS (442.075)<br>').addTo(map);
L.marker([47.6884994500, -122.1559982300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 33 - K7LWH (53.170)<br>RR# 34 - K7LWH (145.490)<br>').addTo(map);
L.marker([47.6814994800, -122.2089996300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 35 - K7LWH (224.360)<br>RR# 36 - K7LWH (441.075)<br>').addTo(map);
L.marker([47.8566093400, -122.2836761500], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>37</div>", iconSize: [25, 25]}) }).bindPopup('RR# 37 - W7FLY (443.925)<br>').addTo(map);
L.marker([47.7376770000, -122.2307900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>38</div>", iconSize: [25, 25]}) }).bindPopup('RR# 38 - NE7MC (442.000)<br>').addTo(map);
L.marker([47.4896147000, -121.9579761000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>39</div>", iconSize: [25, 25]}) }).bindPopup('RR# 39 - WW7STR (146.875)<br>').addTo(map);
L.marker([47.5403984267, -122.0992846800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 40 - WW7STR (224.440)<br>RR# 41 - WW7STR (441.550)<br>RR# 95 - W7RNK (147.995)<br>').addTo(map);
L.marker([47.4883679340, -121.9470088800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 42 - WW7STR (443.050)<br>RR# 71 - K7LED (146.820)<br>RR# 72 - K7LED (224.120)<br>RR# 73 - WA7HJR (444.650)<br>RR# 74 - KB7CNN (1292.200)<br>').addTo(map);
L.marker([47.5559005700, -122.1159973100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>43</div>", iconSize: [25, 25]}) }).bindPopup('RR# 43 - WW7STR (927.2125)<br>').addTo(map);
L.marker([47.0530272050, -122.2944118600], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 44 - N3KPU (145.230)<br>RR# 68 - W7EAT (224.180)<br>').addTo(map);
L.marker([47.1091003400, -122.5530014000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>45</div>", iconSize: [25, 25]}) }).bindPopup('RR# 45 - KE7YYD (442.750)<br>').addTo(map);
L.marker([47.3946000000, -122.5966000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>46</div>", iconSize: [25, 25]}) }).bindPopup('RR# 46 - W7TJL (224.200)<br>').addTo(map);
L.marker([47.3222999600, -122.3130035400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 47 - WA7FW (147.040)<br>RR# 48 - WA7FW (146.760)<br>RR# 49 - WA7FW (442.950)<br>').addTo(map);
L.marker([47.2774009700, -122.2919998200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>50</div>", iconSize: [25, 25]}) }).bindPopup('RR# 50 - WA7FW (442.925)<br>').addTo(map);
L.marker([47.3062355469, -122.3230332117], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 51 - WA7FW (146.840)<br>RR# 52 - WA7FW (443.850)<br>RR# 53 - WA7FW (1290.100)<br>').addTo(map);
L.marker([48.6777000400, -122.8315010050], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 54 - K7SKW (146.740)<br>RR# 55 - K7SKW (444.050)<br>RR# 83 - WA6MPG (224.540)<br>RR# 84 - N7JN (224.480)<br>').addTo(map);
L.marker([48.7821006800, -122.3700027500], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>56</div>", iconSize: [25, 25]}) }).bindPopup('RR# 56 - K7SKW (443.750)<br>').addTo(map);
L.marker([48.8017997750, -122.4614982650], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 57 - K7SKW (147.160)<br>RR# 58 - K7SKW (443.650)<br>').addTo(map);
L.marker([47.3910700000, -122.6079000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>59</div>", iconSize: [25, 25]}) }).bindPopup('RR# 59 - KA7EOC (145.350)<br>').addTo(map);
L.marker([47.2150993300, -123.1009979200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 60 - N7SK (146.720)<br>RR# 61 - N7SK (443.250)<br>RR# 62 - N7SK (927.4125)<br>').addTo(map);
L.marker([47.9979496000, -122.1944999650], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 63 - WA7LAW (147.180)<br>RR# 64 - WA7LAW (444.575)<br>').addTo(map);
L.marker([47.3866150000, -122.8609950000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 65 - NM7E (145.170)<br>RR# 66 - NM7E (224.260)<br>').addTo(map);
L.marker([46.8431010000, -122.3149560000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 67 - W7EAT (146.700)<br>RR# 69 - W7EAT (442.725)<br>').addTo(map);
L.marker([47.1997985800, -121.7559967000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>70</div>", iconSize: [25, 25]}) }).bindPopup('RR# 70 - W7AAO (145.370)<br>').addTo(map);
L.marker([47.6557998700, -122.5479965200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 75 - W7NPC (444.475)<br>RR# 76 - W7NPC (444.5625)<br>RR# 77 - W7NPC (1290.500)<br>').addTo(map);
L.marker([48.0794982900, -123.1019973800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>78</div>", iconSize: [25, 25]}) }).bindPopup('RR# 78 - K6MBY (444.900)<br>').addTo(map);
L.marker([48.0781400000, -123.4120700000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>79</div>", iconSize: [25, 25]}) }).bindPopup('RR# 79 - WF7W (145.130)<br>').addTo(map);
L.marker([48.0069007900, -122.9710006700], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>80</div>", iconSize: [25, 25]}) }).bindPopup('RR# 80 - KC7EQO (442.100)<br>').addTo(map);
L.marker([48.1442985500, -123.6750030500], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>81</div>", iconSize: [25, 25]}) }).bindPopup('RR# 81 - W7FEL (146.760)<br>').addTo(map);
L.marker([47.7565994300, -122.2809982300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>82</div>", iconSize: [25, 25]}) }).bindPopup('RR# 82 - WA7FUS (224.220)<br>').addTo(map);
L.marker([47.2528991700, -122.4440002400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 85 - W7DK (147.280)<br>RR# 86 - W7DK (440.625)<br>').addTo(map);
L.marker([47.2794449000, -122.5123217000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>88</div>", iconSize: [25, 25]}) }).bindPopup('RR# 88 - W7TED (442.450)<br>').addTo(map);
L.marker([46.4879350000, -123.2161347000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>89</div>", iconSize: [25, 25]}) }).bindPopup('RR# 89 - K7CH (52.930)<br>').addTo(map);
L.marker([47.3125800000, -123.3725683000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>90</div>", iconSize: [25, 25]}) }).bindPopup('RR# 90 - K7CH (53.030)<br>').addTo(map);
L.marker([47.0042643000, -122.5398460000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>91</div>", iconSize: [25, 25]}) }).bindPopup('RR# 91 - WA7ROY (444.175)<br>').addTo(map);
L.marker([47.2211990400, -121.8509979200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>92</div>", iconSize: [25, 25]}) }).bindPopup('RR# 92 - N7OEP (53.330)<br>').addTo(map);
L.marker([47.2042999300, -121.9919967700], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 93 - N7OEP (440.075)<br>RR# 94 - N7OEP (443.175)<br>').addTo(map);
L.marker([47.5404497750, -122.3781309250], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 96 - W7AW (53.290)<br>RR# 97 - W7AW (145.130)<br>RR# 98 - W7AW (440.975)<br>RR# 99 - W7AW (441.800)<br>').addTo(map);
L.marker([48.5603981000, -123.1200027500], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>100</div>", iconSize: [25, 25]}) }).bindPopup('RR# 100 - N7JN (146.700)<br>').addTo(map);
L.marker([48.5343017600, -123.0169982900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 101 - N7JN (145.250)<br>RR# 102 - N7JN (442.4625)<br>').addTo(map);
L.marker([48.2249984700, -122.5000000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 103 - W7PIG (147.360)<br>RR# 104 - W7PIG (441.050)<br>').addTo(map);
L.marker([46.9753990200, -123.8160018900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>105</div>", iconSize: [25, 25]}) }).bindPopup('RR# 105 - W7ZA (147.160)<br>').addTo(map);
L.marker([47.4128990200, -123.8799972500], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>106</div>", iconSize: [25, 25]}) }).bindPopup('RR# 106 - W7ZA (146.900)<br>').addTo(map);
L.marker([46.9730987500, -123.1350021400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>107</div>", iconSize: [25, 25]}) }).bindPopup('RR# 107 - K7CPR (145.470)<br>').addTo(map);
L.marker([48.6883764275, -122.3612499225], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 108 - W7ECG (146.450)<br>RR# 109 - W7ECG (224.160)<br>RR# 110 - W7ECG (440.475)<br>RR# 112 - W7ECG (442.250)<br>').addTo(map);
L.marker([48.8614073000, -122.6178286100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 111 - W7ECG (440.7375)<br>RR# 113 - W7ECG (442.825)<br>').addTo(map);
L.marker([48.7361205700, -122.4810043900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>114</div>", iconSize: [25, 25]}) }).bindPopup('RR# 114 - W7BFD (442.300)<br>').addTo(map);
L.marker([47.8614800000, -122.2837100000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>115</div>", iconSize: [25, 25]}) }).bindPopup('RR# 115 - WA7DEM (146.780)<br>').addTo(map);
L.marker([48.1200000000, -122.2400000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 116 - WA7DEM (224.380)<br>RR# 122 - K7MLR (444.200)<br>').addTo(map);
L.marker([47.8329000000, -122.1239700000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>117</div>", iconSize: [25, 25]}) }).bindPopup('RR# 117 - WA7DEM (442.975)<br>').addTo(map);
L.marker([47.7976000000, -122.3124000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>118</div>", iconSize: [25, 25]}) }).bindPopup('RR# 118 - WA7DEM (443.725)<br>').addTo(map);
L.marker([48.1369500000, -121.9814000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>119</div>", iconSize: [25, 25]}) }).bindPopup('RR# 119 - WA7DEM (146.92)<br>').addTo(map);
L.marker([47.8035000000, -122.3346000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>120</div>", iconSize: [25, 25]}) }).bindPopup('RR# 120 - WA7DEM (444.025)<br>').addTo(map);
L.marker([48.2494400000, -121.5694900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>121</div>", iconSize: [25, 25]}) }).bindPopup('RR# 121 - WA7DEM (444.300)<br>').addTo(map);
L.marker([47.3853730000, -122.0614967000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 123 - KF7NPL (147.260)<br>RR# 124 - KF7NPL (442.675)<br>').addTo(map);

</script>
