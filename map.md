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

L.marker([47.6238485020, -122.3151189440], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 1 - WW7PSR (146.960)<br>RR# 2 - WW7PSR (52.870)<br>RR# 13 - W7ACS (442.875)<br>RR# 137 - W7ACS (442.875)<br>RR# 141 - W7ACS (443.200)<br>').addTo(map);
L.marker([47.6324996900, -122.3560028100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>3</div>", iconSize: [25, 25]}) }).bindPopup('RR# 3 - WW7SEA (444.700)<br>').addTo(map);
L.marker([47.5404380333, -122.3780892333], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 4 - W7AW (53.290)<br>RR# 5 - W7AW (145.130)<br>RR# 6 - W7AW (441.800)<br>').addTo(map);
L.marker([47.2528991700, -122.4440002400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 7 - W7DK (147.280)<br>RR# 9 - W7DK (145.210)<br>').addTo(map);
L.marker([47.7719675667, -122.2809634000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 8 - W7DK (440.625)<br>RR# 16 - W7ACS (440.600)<br>RR# 140 - W7ACS (440.600)<br>').addTo(map);
L.marker([46.8429336533, -122.7643330900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 10 - W7DK (147.380)<br>RR# 69 - NT7H (224.460)<br>RR# 70 - NT7H (441.400)<br>').addTo(map);
L.marker([47.6031132000, -122.3187965000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>11</div>", iconSize: [25, 25]}) }).bindPopup('RR# 11 - W7ACS (442.300)<br>').addTo(map);
L.marker([47.6045123250, -122.3304144150], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 12 - W7ACS (444.550)<br>RR# 133 - W7ACS (444.550)<br>').addTo(map);
L.marker([47.6509388500, -122.3904118500], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 14 - W7ACS (443.475)<br>RR# 138 - W7ACS (443.475)<br>').addTo(map);
L.marker([47.6906790000, -122.3175873500], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 15 - W7ACS (443.650)<br>RR# 139 - W7ACS (443.650)<br>').addTo(map);
L.marker([47.5207400000, -122.3433148000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>17</div>", iconSize: [25, 25]}) }).bindPopup('RR# 17 - W7ACS (443.200)<br>').addTo(map);
L.marker([47.6884994500, -122.1559982300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 18 - K7LWH (53.170)<br>RR# 19 - K7LWH (145.490)<br>').addTo(map);
L.marker([47.6814994800, -122.2089996300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 20 - K7LWH (224.360)<br>RR# 21 - K7LWH (441.075)<br>').addTo(map);
L.marker([47.5683670000, -122.2207290000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 22 - W7MIR (147.160)<br>RR# 23 - W7MIR (440.150)<br>').addTo(map);
L.marker([48.5833015400, -122.1449966400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>24</div>", iconSize: [25, 25]}) }).bindPopup('RR# 24 - N7GDE (145.190)<br>').addTo(map);
L.marker([47.5494494900, -122.7834260000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 25 - KC7Z (146.620)<br>RR# 26 - KC7Z (442.650)<br>RR# 27 - KC7Z (441.175)<br>').addTo(map);
L.marker([47.6021162500, -122.6173161000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>28</div>", iconSize: [25, 25]}) }).bindPopup('RR# 28 - KC7Z (444.075)<br>').addTo(map);
L.marker([47.6555143000, -122.9594265000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 29 - WW7RA (146.620)<br>RR# 30 - WW7RA (442.65)<br>').addTo(map);
L.marker([48.1170005800, -122.7600021400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>31</div>", iconSize: [25, 25]}) }).bindPopup('RR# 31 - W7JCR (145.150)<br>').addTo(map);
L.marker([48.0583000200, -122.6880035400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>32</div>", iconSize: [25, 25]}) }).bindPopup('RR# 32 - AA7MI (440.725)<br>').addTo(map);
L.marker([47.2150993300, -123.1009979200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 33 - N7SK (146.720)<br>RR# 34 - N7SK (443.250)<br>RR# 35 - N7SK (927.4125)<br>').addTo(map);
L.marker([47.3222999600, -122.3130035400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 36 - WA7FW (146.760)<br>RR# 37 - WA7FW (442.950)<br>').addTo(map);
L.marker([47.2774009700, -122.2919998200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>38</div>", iconSize: [25, 25]}) }).bindPopup('RR# 38 - WA7FW (442.925)<br>').addTo(map);
L.marker([48.0069007900, -122.9710006700], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>39</div>", iconSize: [25, 25]}) }).bindPopup('RR# 39 - KC7EQO (442.100)<br>').addTo(map);
L.marker([47.1997985800, -121.7559967000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>40</div>", iconSize: [25, 25]}) }).bindPopup('RR# 40 - W7AAO (145.370)<br>').addTo(map);
L.marker([46.8431010000, -122.3149560000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 41 - W7EAT (146.700)<br>RR# 43 - W7EAT (442.725)<br>').addTo(map);
L.marker([47.0530272050, -122.2944118600], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 42 - W7EAT (224.180)<br>RR# 78 - N3KPU (145.230)<br>').addTo(map);
L.marker([47.7376770000, -122.2307900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>44</div>", iconSize: [25, 25]}) }).bindPopup('RR# 44 - NE7MC (442.000)<br>').addTo(map);
L.marker([47.5404491400, -122.0989990200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 45 - WW7STR (224.440)<br>RR# 46 - WW7STR (441.550)<br>').addTo(map);
L.marker([47.4883468833, -121.9470157333], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 47 - WW7STR (443.050)<br>RR# 97 - K7LED (146.820)<br>RR# 98 - K7LED (224.120)<br>').addTo(map);
L.marker([47.5559005700, -122.1159973100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>48</div>", iconSize: [25, 25]}) }).bindPopup('RR# 48 - WW7STR (927.2125)<br>').addTo(map);
L.marker([48.5603981000, -123.1200027500], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>49</div>", iconSize: [25, 25]}) }).bindPopup('RR# 49 - N7JN (146.700)<br>').addTo(map);
L.marker([48.6777992200, -122.8310012800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 50 - N7JN (224.480)<br>RR# 51 - N7JN (443.450)<br>').addTo(map);
L.marker([47.2211990400, -121.8509979200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>52</div>", iconSize: [25, 25]}) }).bindPopup('RR# 52 - N7OEP (53.330)<br>').addTo(map);
L.marker([47.2042999300, -121.9919967700], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 53 - N7OEP (440.075)<br>RR# 54 - N7OEP (443.175)<br>').addTo(map);
L.marker([47.7724990800, -122.9300003100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>55</div>", iconSize: [25, 25]}) }).bindPopup('RR# 55 - K7DK (440.950)<br>').addTo(map);
L.marker([46.8672981300, -122.2669982900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 56 - W7PFR (53.410)<br>RR# 57 - W7PFR (443.975)<br>').addTo(map);
L.marker([47.5038986200, -121.9759979200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 58 - K7NWS (442.075)<br>RR# 59 - K7NWS (145.330)<br>RR# 60 - K7NWS (224.340)<br>').addTo(map);
L.marker([47.3910700000, -122.6079000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>61</div>", iconSize: [25, 25]}) }).bindPopup('RR# 61 - KA7EOC (145.350)<br>').addTo(map);
L.marker([47.9979496000, -122.1944999650], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 62 - WA7LAW (147.180)<br>RR# 63 - WA7LAW (444.575)<br>').addTo(map);
L.marker([47.5301017800, -122.0329971300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>64</div>", iconSize: [25, 25]}) }).bindPopup('RR# 64 - N9VW (53.830)<br>').addTo(map);
L.marker([47.5420280000, -122.1091100000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 65 - KC7RAS (147.100)<br>RR# 66 - N6OBY (443.325)<br>RR# 67 - WA7ACS (440.175)<br>').addTo(map);
L.marker([47.0279998800, -122.8970031700], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>68</div>", iconSize: [25, 25]}) }).bindPopup('RR# 68 - NT7H (147.360)<br>').addTo(map);
L.marker([47.8439700000, -122.5427500000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>71</div>", iconSize: [25, 25]}) }).bindPopup('RR# 71 - K7GKR (444.725)<br>').addTo(map);
L.marker([48.2125015300, -122.7050018300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>72</div>", iconSize: [25, 25]}) }).bindPopup('RR# 72 - W7AVM (146.860)<br>').addTo(map);
L.marker([48.0401001000, -122.4059982300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>73</div>", iconSize: [25, 25]}) }).bindPopup('RR# 73 - W7AVM (147.220)<br>').addTo(map);
L.marker([47.4508018500, -122.2870025600], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 74 - NC7G (146.660)<br>RR# 75 - WA7ST (443.100)<br>').addTo(map);
L.marker([47.4726950000, -122.3454480000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>76</div>", iconSize: [25, 25]}) }).bindPopup('RR# 76 - W7BUR (441.125)<br>').addTo(map);
L.marker([47.4023300000, -122.3035600000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>77</div>", iconSize: [25, 25]}) }).bindPopup('RR# 77 - WA7DES (443.700)<br>').addTo(map);
L.marker([47.1091003400, -122.5530014000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>79</div>", iconSize: [25, 25]}) }).bindPopup('RR# 79 - KE7YYD (442.750)<br>').addTo(map);
L.marker([47.7542991600, -122.1630020100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 80 - K6RFK (147.340)<br>RR# 81 - K6RFK (442.775)<br>').addTo(map);
L.marker([46.9730987500, -123.1350021400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>82</div>", iconSize: [25, 25]}) }).bindPopup('RR# 82 - K7CPR (145.470)<br>').addTo(map);
L.marker([48.0982722000, -122.5731977000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>83</div>", iconSize: [25, 25]}) }).bindPopup('RR# 83 - N7KN (441.425)<br>').addTo(map);
L.marker([48.2249984700, -122.5000000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 84 - W7PIG (147.360)<br>RR# 86 - W7PIG (441.050)<br>').addTo(map);
L.marker([48.1915016200, -122.5149993900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>85</div>", iconSize: [25, 25]}) }).bindPopup('RR# 85 - W7PIG (223.880)<br>').addTo(map);
L.marker([46.4881670000, -123.2147800000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 87 - K7CH (53.030)<br>RR# 89 - KK7DFM (444.450)<br>').addTo(map);
L.marker([47.0057350000, -122.9449420000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>88</div>", iconSize: [25, 25]}) }).bindPopup('RR# 88 - KK7DFL (145.275)<br>').addTo(map);
L.marker([48.6800797000, -122.8425501000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 90 - K7SKW (146.740)<br>RR# 91 - K7SKW (444.050)<br>').addTo(map);
L.marker([48.7884669000, -122.3852150000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>92</div>", iconSize: [25, 25]}) }).bindPopup('RR# 92 - K7SKW (443.750)<br>').addTo(map);
L.marker([48.8017863000, -122.4625177000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>93</div>", iconSize: [25, 25]}) }).bindPopup('RR# 93 - K7SKW (147.160)<br>').addTo(map);
L.marker([47.6241000000, -117.1750000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>94</div>", iconSize: [25, 25]}) }).bindPopup('RR# 94 - W7TRF (145.210)<br>').addTo(map);
L.marker([47.6068000000, -117.2034000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>95</div>", iconSize: [25, 25]}) }).bindPopup('RR# 95 - W7TRF (443.475)<br>').addTo(map);
L.marker([47.8566093400, -122.2836761500], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>96</div>", iconSize: [25, 25]}) }).bindPopup('RR# 96 - W7FLY (443.925)<br>').addTo(map);
L.marker([46.0765762800, -122.8034604000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>99</div>", iconSize: [25, 25]}) }).bindPopup('RR# 99 - W7MSH (444.725)<br>').addTo(map);
L.marker([47.0042643000, -122.5398460000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>100</div>", iconSize: [25, 25]}) }).bindPopup('RR# 100 - WA7ROY (444.175)<br>').addTo(map);
L.marker([47.5778007500, -122.3089981100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>101</div>", iconSize: [25, 25]}) }).bindPopup('RR# 101 - WW7MST (146.900)<br>').addTo(map);
L.marker([47.5526008600, -122.3010025000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>102</div>", iconSize: [25, 25]}) }).bindPopup('RR# 102 - WW7MST (443.550)<br>').addTo(map);
L.marker([47.6748100000, -122.0534360000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>103</div>", iconSize: [25, 25]}) }).bindPopup('RR# 103 - W7DX (147.000)<br>').addTo(map);
L.marker([48.1256990000, -121.9844964000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>104</div>", iconSize: [25, 25]}) }).bindPopup('RR# 104 - WA7DEM (146.920)<br>').addTo(map);
L.marker([48.1227936000, -122.2567359000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 105 - WA7DEM (224.380)<br>RR# 106 - WA7DEM (444.200)<br>').addTo(map);
L.marker([47.8636169000, -122.2786477000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>107</div>", iconSize: [25, 25]}) }).bindPopup('RR# 107 - WA7DEM (146.780)<br>').addTo(map);
L.marker([47.8288566000, -122.0739169000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>108</div>", iconSize: [25, 25]}) }).bindPopup('RR# 108 - WA7DEM (442.975)<br>').addTo(map);
L.marker([47.8025185000, -122.3228347000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>109</div>", iconSize: [25, 25]}) }).bindPopup('RR# 109 - WA7DEM (443.725)<br>').addTo(map);
L.marker([47.8028705000, -122.3334163000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>110</div>", iconSize: [25, 25]}) }).bindPopup('RR# 110 - WA7DEM (444.025)<br>').addTo(map);
L.marker([47.6576742000, -116.9684792000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 111 - N7IRG (53.390)<br>RR# 112 - N7IRG (147.280)<br>RR# 113 - N7IRG (442.950)<br>').addTo(map);
L.marker([47.3634565000, -116.4122550000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>114</div>", iconSize: [25, 25]}) }).bindPopup('RR# 114 - N7IRG (147.260)<br>').addTo(map);
L.marker([47.5642862000, -115.8521100000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>115</div>", iconSize: [25, 25]}) }).bindPopup('RR# 115 - N7IRG (147.180)<br>').addTo(map);
L.marker([48.0787224000, -116.9537798000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 116 - N7IRG (145.490)<br>RR# 117 - N7IRG (444.550)<br>').addTo(map);
L.marker([48.6101410000, -116.2600576000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>118</div>", iconSize: [25, 25]}) }).bindPopup('RR# 118 - N7IRG (146.960)<br>').addTo(map);
L.marker([48.6063229000, -116.9518883000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>119</div>", iconSize: [25, 25]}) }).bindPopup('RR# 119 - N7IRG (145.410)<br>').addTo(map);
L.marker([48.5457000700, -119.2360000600], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>120</div>", iconSize: [25, 25]}) }).bindPopup('RR# 120 - WA7MV (147.320)<br>').addTo(map);
L.marker([48.3634784000, -120.1223030000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>121</div>", iconSize: [25, 25]}) }).bindPopup('RR# 121 - WA7MV (146.720)<br>').addTo(map);
L.marker([48.3176002500, -120.1149978600], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>122</div>", iconSize: [25, 25]}) }).bindPopup('RR# 122 - WA7MV (444.800)<br>').addTo(map);
L.marker([46.5139007600, -121.2080001800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>123</div>", iconSize: [25, 25]}) }).bindPopup('RR# 123 - WA7SAR (146.860)<br>').addTo(map);
L.marker([46.0633010900, -121.4240036000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>124</div>", iconSize: [25, 25]}) }).bindPopup('RR# 124 - WA7SAR (147.080)<br>').addTo(map);
L.marker([46.5222015400, -120.3330001800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>125</div>", iconSize: [25, 25]}) }).bindPopup('RR# 125 - WA7SAR (444.600)<br>').addTo(map);
L.marker([47.0731250000, -121.0786900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>126</div>", iconSize: [25, 25]}) }).bindPopup('RR# 126 - WA7SAR (145.270)<br>').addTo(map);
L.marker([46.6414000000, -120.3967000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>127</div>", iconSize: [25, 25]}) }).bindPopup('RR# 127 - WA7SAR (147.080)<br>').addTo(map);
L.marker([47.1523017900, -120.5640029900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 128 - K7RHT (147.000)<br>RR# 129 - K7RHT (444.450)<br>').addTo(map);
L.marker([47.6489450000, -121.9160700000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>130</div>", iconSize: [25, 25]}) }).bindPopup('RR# 130 - KE7GFZ (441.850)<br>').addTo(map);
L.marker([47.7649993900, -121.9390029900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>131</div>", iconSize: [25, 25]}) }).bindPopup('RR# 131 - KE7GFZ (443.250)<br>').addTo(map);
L.marker([47.6299300000, -121.9500800000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>132</div>", iconSize: [25, 25]}) }).bindPopup('RR# 132 - WA7TBP (223.960)<br>').addTo(map);
L.marker([47.5885137000, -122.3166969000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 134 - W7ACS (440.525)<br>RR# 135 - W7ACS (442.300)<br>').addTo(map);
L.marker([47.6200881000, -122.3122380000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>136</div>", iconSize: [25, 25]}) }).bindPopup('RR# 136 - W7ACS (443.025)<br>').addTo(map);
L.marker([47.8847007800, -120.1569976800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>142</div>", iconSize: [25, 25]}) }).bindPopup('RR# 142 - K7YR (146.820)<br>').addTo(map);
L.marker([47.8535995500, -119.8730011000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 143 - K7SMX (147.100)<br>RR# 144 - K7SMX (444.525)<br>').addTo(map);

</script>
