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
var map = L.map('map').setView([47.63, -120], 6);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

L.marker([47.6395000000, -122.3693000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>1</div>", iconSize: [25, 25]}) }).bindPopup('RR# 1 - WW7PSR (146.960)<br>').addTo(map);
L.marker([47.6238100000, -122.3153050000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 2 - WW7PSR (52.870)<br>RR# 100 - W7ACS (442.875)<br>').addTo(map);
L.marker([46.8354000000, -122.2878000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 3 - W7PFR (53.410)<br>RR# 4 - W7PFR (443.975)<br>').addTo(map);
L.marker([47.6322000000, -122.3539000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>5</div>", iconSize: [25, 25]}) }).bindPopup('RR# 5 - WW7SEA (444.425)<br>').addTo(map);
L.marker([47.6370100000, -122.3488000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>6</div>", iconSize: [25, 25]}) }).bindPopup('RR# 6 - WW7SEA (444.700)<br>').addTo(map);
L.marker([47.6745900000, -122.0539300000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>7</div>", iconSize: [25, 25]}) }).bindPopup('RR# 7 - W7DX (147.000)<br>').addTo(map);
L.marker([48.1247000000, -122.7651000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>8</div>", iconSize: [25, 25]}) }).bindPopup('RR# 8 - W7JCR (145.150)<br>').addTo(map);
L.marker([48.0402600000, -122.6877500000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>9</div>", iconSize: [25, 25]}) }).bindPopup('RR# 9 - AA7MI (440.725)<br>').addTo(map);
L.marker([47.8614800000, -122.2837100000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>10</div>", iconSize: [25, 25]}) }).bindPopup('RR# 10 - WA7DEM (146.775)<br>').addTo(map);
L.marker([48.1369500000, -121.9814000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>11</div>", iconSize: [25, 25]}) }).bindPopup('RR# 11 - WA7DEM (146.925)<br>').addTo(map);
L.marker([48.1200000000, -122.2400000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>12</div>", iconSize: [25, 25]}) }).bindPopup('RR# 12 - WA7DEM (224.380)<br>').addTo(map);
L.marker([47.8329000000, -122.1239700000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>13</div>", iconSize: [25, 25]}) }).bindPopup('RR# 13 - WA7DEM (442.975)<br>').addTo(map);
L.marker([47.7976000000, -122.3124000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>14</div>", iconSize: [25, 25]}) }).bindPopup('RR# 14 - WA7DEM (443.725)<br>').addTo(map);
L.marker([47.8035000000, -122.3346000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>15</div>", iconSize: [25, 25]}) }).bindPopup('RR# 15 - WA7DEM (444.025)<br>').addTo(map);
L.marker([48.1225280000, -122.2433800000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>16</div>", iconSize: [25, 25]}) }).bindPopup('RR# 16 - WA7DEM (444.200)<br>').addTo(map);
L.marker([48.2494400000, -122.5691600000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>17</div>", iconSize: [25, 25]}) }).bindPopup('RR# 17 - WA7DEM (444.300)<br>').addTo(map);
L.marker([47.5683800000, -122.2207800000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 18 - W7MIR (147.160)<br>RR# 19 - W7MIR (440.150)<br>').addTo(map);
L.marker([46.1828000000, -122.9578000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 20 - W7DG (147.100)<br>RR# 22 - W7DG (224.140)<br>RR# 23 - W7DG (444.900)<br>').addTo(map);
L.marker([45.9700000000, -122.6700000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>21</div>", iconSize: [25, 25]}) }).bindPopup('RR# 21 - W7DG (147.300)<br>').addTo(map);
L.marker([47.7253000000, -122.1189000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>24</div>", iconSize: [25, 25]}) }).bindPopup('RR# 24 - K6RFK (147.340)<br>').addTo(map);
L.marker([47.7433000000, -122.1259000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>25</div>", iconSize: [25, 25]}) }).bindPopup('RR# 25 - K6RFK (442.775)<br>').addTo(map);
L.marker([47.2038700000, -122.7956400000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>26</div>", iconSize: [25, 25]}) }).bindPopup('RR# 26 - W7AAO (145.370)<br>').addTo(map);
L.marker([47.2136000000, -122.2653000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>27</div>", iconSize: [25, 25]}) }).bindPopup('RR# 27 - W7AAO (146.640)<br>').addTo(map);
L.marker([47.1167000000, -121.8925000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>28</div>", iconSize: [25, 25]}) }).bindPopup('RR# 28 - W7AAO (927.850)<br>').addTo(map);
L.marker([47.2800000000, -122.2900000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>29</div>", iconSize: [25, 25]}) }).bindPopup('RR# 29 - WA7FW (146.760)<br>').addTo(map);
L.marker([47.3246630000, -122.3260400000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>30</div>", iconSize: [25, 25]}) }).bindPopup('RR# 30 - WA7FW (147.040)<br>').addTo(map);
L.marker([47.3200000000, -122.3300000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 31 - WA7FW (442.925)<br>RR# 32 - WA7FW (442.950)<br>').addTo(map);
L.marker([48.0066600000, -122.9726700000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>33</div>", iconSize: [25, 25]}) }).bindPopup('RR# 33 - KC7EQO (442.100)<br>').addTo(map);
L.marker([47.5478800000, -122.8073000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 34 - KC7Z (146.620)<br>RR# 35 - KC7Z (442.650)<br>').addTo(map);
L.marker([47.6021200000, -122.6174600000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>36</div>", iconSize: [25, 25]}) }).bindPopup('RR# 36 - KC7Z (444.075)<br>').addTo(map);
L.marker([47.5087500000, -121.9851900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 37 - K7NWS (145.330)<br>RR# 38 - K7NWS (224.340)<br>').addTo(map);
L.marker([47.5100000000, -121.9900000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>39</div>", iconSize: [25, 25]}) }).bindPopup('RR# 39 - K7NWS (442.075)<br>').addTo(map);
L.marker([46.4882000000, -123.2148000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 40 - K7CH (53.030)<br>RR# 54 - K7CH (444.450)<br>').addTo(map);
L.marker([47.5416296667, -122.1091766667], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 44 - N9VW (443.325)<br>RR# 45 - KC7RAS (147.100)<br>RR# 69 - K7PP (443.400)<br>').addTo(map);
L.marker([48.2261900000, -122.5019000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>46</div>", iconSize: [25, 25]}) }).bindPopup('RR# 46 - W7PIG (147.360)<br>').addTo(map);
L.marker([48.2247000000, -122.4989000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>47</div>", iconSize: [25, 25]}) }).bindPopup('RR# 47 - W7PIG (223.880)<br>').addTo(map);
L.marker([48.0800000000, -122.3775000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>48</div>", iconSize: [25, 25]}) }).bindPopup('RR# 48 - W7PIG (441.050)<br>').addTo(map);
L.marker([47.6299300000, -121.9500800000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>49</div>", iconSize: [25, 25]}) }).bindPopup('RR# 49 - WA7TBP (223.960)<br>').addTo(map);
L.marker([47.7600000000, -122.3500000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>50</div>", iconSize: [25, 25]}) }).bindPopup('RR# 50 - W7AUX (224.020)<br>').addTo(map);
L.marker([47.7561900000, -122.3457500000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 51 - W7AUX (440.300)<br>RR# 53 - W7AUX (927.638)<br>').addTo(map);
L.marker([47.7680000000, -122.3531000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>52</div>", iconSize: [25, 25]}) }).bindPopup('RR# 52 - W7AUX (442.825)<br>').addTo(map);
L.marker([47.4880500000, -121.9469400000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 55 - K7LED (146.820)<br>RR# 56 - K7LED (224.120)<br>').addTo(map);
L.marker([47.5404706667, -122.3778903333], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 57 - W7AW (53.290)<br>RR# 58 - W7AW (145.130)<br>RR# 59 - W7AW (441.800)<br>').addTo(map);
L.marker([48.5947460000, -122.1594200000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>60</div>", iconSize: [25, 25]}) }).bindPopup('RR# 60 - N7GDE (145.190)<br>').addTo(map);
L.marker([47.2072000000, -123.1183000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 61 - N7SK (146.720)<br>RR# 62 - N7SK (443.250)<br>RR# 63 - N7SK (927.413)<br>').addTo(map);
L.marker([47.9980140000, -122.1945600000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 64 - WA7LAW (147.180)<br>RR# 65 - WA7LAW (444.575)<br>').addTo(map);
L.marker([47.7500000000, -124.1766600000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>66</div>", iconSize: [25, 25]}) }).bindPopup('RR# 66 - K7PP (147.280)<br>').addTo(map);
L.marker([47.5492585000, -122.7837200000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 67 - K7PP (441.200)<br>RR# 70 - KC7Z (441.175)<br>').addTo(map);
L.marker([46.4614300000, -123.5462000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>68</div>", iconSize: [25, 25]}) }).bindPopup('RR# 68 - K7PP (441.300)<br>').addTo(map);
L.marker([48.5457000700, -119.2360000600], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>71</div>", iconSize: [25, 25]}) }).bindPopup('RR# 71 - WA7MV (147.320)<br>').addTo(map);
L.marker([48.3634784000, -120.1223030000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>72</div>", iconSize: [25, 25]}) }).bindPopup('RR# 72 - WA7MV (146.720)<br>').addTo(map);
L.marker([48.3176002500, -120.1149978600], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>73</div>", iconSize: [25, 25]}) }).bindPopup('RR# 73 - WA7MV (444.800)<br>').addTo(map);
L.marker([47.6637000000, -122.1665000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 74 - K7LWH (145.490)<br>RR# 75 - K7LWH (224.360)<br>RR# 76 - K7LWH (441.075)<br>RR# 78 - K7LWH (53.170)<br>').addTo(map);
L.marker([47.5788993800, -117.2959976200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>79</div>", iconSize: [25, 25]}) }).bindPopup('RR# 79 - WR7VHF (146.880)<br>').addTo(map);
L.marker([47.6587982200, -117.4260025000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>80</div>", iconSize: [25, 25]}) }).bindPopup('RR# 80 - WR7VHF (147.340)<br>').addTo(map);
L.marker([47.9193992600, -117.1139984100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>81</div>", iconSize: [25, 25]}) }).bindPopup('RR# 81 - WR7VHF (444.600)<br>').addTo(map);
L.marker([48.0788002000, -116.9540023800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>82</div>", iconSize: [25, 25]}) }).bindPopup('RR# 82 - K7JEP (145.490)<br>').addTo(map);
L.marker([48.0168468000, -116.9838096000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>83</div>", iconSize: [25, 25]}) }).bindPopup('RR# 83 - K7JEP (444.550)<br>').addTo(map);
L.marker([47.1523017900, -120.5640029900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 84 - K7RHT (147.000)<br>RR# 85 - K7RHT (444.450)<br>').addTo(map);
L.marker([46.6539993300, -120.5299987800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>86</div>", iconSize: [25, 25]}) }).bindPopup('RR# 86 - KC7VQR (147.240)<br>').addTo(map);
L.marker([45.7415084800, -121.6861877400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>87</div>", iconSize: [25, 25]}) }).bindPopup('RR# 87 - W6TQF (440.325)<br>').addTo(map);
L.marker([45.9347991900, -121.8199996900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 88 - KB7APU (145.250)<br>RR# 127 - KB7APU (145.250)<br>').addTo(map);
L.marker([46.8100013700, -119.8820037800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>89</div>", iconSize: [25, 25]}) }).bindPopup('RR# 89 - N7MHE (145.350)<br>').addTo(map);
L.marker([43.9760707000, -116.4075535000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 90 - K7SWI (224.940)<br>RR# 91 - K7SWI (444.375)<br>RR# 92 - N7UBO (146.740)<br>').addTo(map);
L.marker([43.4109190000, -116.5895690000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>93</div>", iconSize: [25, 25]}) }).bindPopup('RR# 93 - KI7PWR (146.920)<br>').addTo(map);
L.marker([47.7376770000, -122.2307900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>94</div>", iconSize: [25, 25]}) }).bindPopup('RR# 94 - NE7MC (442.000)<br>').addTo(map);
L.marker([47.3866050000, -122.8609900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 95 - NM7E (145.170)<br>RR# 96 - NM7E (224.260)<br>').addTo(map);
L.marker([47.5887800000, -122.3176500000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 97 - W7ACS (440.525)<br>RR# 99 - W7ACS (442.300)<br>').addTo(map);
L.marker([47.7719300000, -122.2809900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>98</div>", iconSize: [25, 25]}) }).bindPopup('RR# 98 - W7ACS (440.600)<br>').addTo(map);
L.marker([47.6190100000, -122.3124700000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>101</div>", iconSize: [25, 25]}) }).bindPopup('RR# 101 - W7ACS (443.025)<br>').addTo(map);
L.marker([47.5207500000, -122.3434100000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>102</div>", iconSize: [25, 25]}) }).bindPopup('RR# 102 - W7ACS (443.200)<br>').addTo(map);
L.marker([47.6507300000, -122.3925800000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>103</div>", iconSize: [25, 25]}) }).bindPopup('RR# 103 - W7ACS (443.475)<br>').addTo(map);
L.marker([47.6909000000, -122.3196300000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>104</div>", iconSize: [25, 25]}) }).bindPopup('RR# 104 - W7ACS (443.650)<br>').addTo(map);
L.marker([47.6047220000, -122.3305500000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>105</div>", iconSize: [25, 25]}) }).bindPopup('RR# 105 - W7ACS (444.550)<br>').addTo(map);
L.marker([47.0005780000, -122.9455700000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>106</div>", iconSize: [25, 25]}) }).bindPopup('RR# 106 - KK7DFL (145.275)<br>').addTo(map);
L.marker([47.2786110000, -122.5127700000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>107</div>", iconSize: [25, 25]}) }).bindPopup('RR# 107 - W7DK (145.210)<br>').addTo(map);
L.marker([47.2483300000, -122.4845600000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 108 - W7DK (147.280)<br>RR# 110 - W7DK (440.625)<br>').addTo(map);
L.marker([46.8425800000, -122.7640600000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>109</div>", iconSize: [25, 25]}) }).bindPopup('RR# 109 - W7DK (147.380)<br>').addTo(map);
L.marker([47.8560000000, -122.2830000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>111</div>", iconSize: [25, 25]}) }).bindPopup('RR# 111 - W7FLY (443.925)<br>').addTo(map);
L.marker([47.4508700000, -122.2868000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>112</div>", iconSize: [25, 25]}) }).bindPopup('RR# 112 - WA7ST (443.100)<br>').addTo(map);
L.marker([47.4500000000, -122.2900000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>113</div>", iconSize: [25, 25]}) }).bindPopup('RR# 113 - NC7G (146.660)<br>').addTo(map);
L.marker([47.4728000000, -122.3456000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>114</div>", iconSize: [25, 25]}) }).bindPopup('RR# 114 - W7BUR (441.125)<br>').addTo(map);
L.marker([47.4023300000, -122.3035600000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>115</div>", iconSize: [25, 25]}) }).bindPopup('RR# 115 - WA7DES (443.700)<br>').addTo(map);
L.marker([47.2086100000, -119.3191700000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>116</div>", iconSize: [25, 25]}) }).bindPopup('RR# 116 - N7MHE (146.70)<br>').addTo(map);
L.marker([47.6558000000, -122.5475000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>117</div>", iconSize: [25, 25]}) }).bindPopup('RR# 117 - W7NPC (444.475)<br>').addTo(map);
L.marker([47.3922000000, -122.3251000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>118</div>", iconSize: [25, 25]}) }).bindPopup('RR# 118 - WA6PMX (224.420)<br>').addTo(map);
L.marker([47.7660600000, -122.6599000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>119</div>", iconSize: [25, 25]}) }).bindPopup('RR# 119 - WA6PMX (442.200)<br>').addTo(map);
L.marker([45.9937300000, -118.1805300000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>120</div>", iconSize: [25, 25]}) }).bindPopup('RR# 120 - KB7ARA (147.280)<br>').addTo(map);
L.marker([46.7323989900, -117.0000000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>121</div>", iconSize: [25, 25]}) }).bindPopup('RR# 121 - KA7FVV (147.320)<br>').addTo(map);
L.marker([48.1813900000, -117.9891700000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>122</div>", iconSize: [25, 25]}) }).bindPopup('RR# 122 - N7WRR (147.360)<br>').addTo(map);
L.marker([47.5749500000, -117.0811300000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>123</div>", iconSize: [25, 25]}) }).bindPopup('RR# 123 - N7WRQ (147.380)<br>').addTo(map);
L.marker([47.2193600000, -121.8422566667], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 124 - N7OEP (440.075)<br>RR# 125 - N7OEP (443.175)<br>RR# 126 - N7OEP (53.330)<br>').addTo(map);
L.marker([48.0697020000, -122.5803300000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>128</div>", iconSize: [25, 25]}) }).bindPopup('RR# 128 - N7KN (441.425)<br>').addTo(map);

</script>
