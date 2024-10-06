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

L.marker([47.6238670367, -122.3150024400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 1 - WW7PSR (146.960)<br>RR# 2 - WW7PSR (52.870)<br>RR# 13 - W7ACS (442.875)<br>').addTo(map);
L.marker([47.6324996900, -122.3560028100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>3</div>", iconSize: [25, 25]}) }).bindPopup('RR# 3 - WW7SEA (444.700)<br>').addTo(map);
L.marker([47.5404380333, -122.3780892333], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 4 - W7AW (53.290)<br>RR# 5 - W7AW (145.130)<br>RR# 6 - W7AW (441.800)<br>').addTo(map);
L.marker([47.2528991700, -122.4440002400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 7 - W7DK (147.280)<br>RR# 8 - W7DK (440.625)<br>RR# 9 - W7DK (145.210)<br>').addTo(map);
L.marker([46.8429336533, -122.7643330900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 10 - W7DK (147.380)<br>RR# 66 - NT7H (224.460)<br>RR# 67 - NT7H (441.400)<br>').addTo(map);
L.marker([47.6031132000, -122.3187965000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>11</div>", iconSize: [25, 25]}) }).bindPopup('RR# 11 - W7ACS (442.300)<br>').addTo(map);
L.marker([47.6043014500, -122.3300018300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>12</div>", iconSize: [25, 25]}) }).bindPopup('RR# 12 - W7ACS (444.550)<br>').addTo(map);
L.marker([47.6510101000, -122.3893988000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>14</div>", iconSize: [25, 25]}) }).bindPopup('RR# 14 - W7ACS (443.475)<br>').addTo(map);
L.marker([47.6901190000, -122.3177855000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>15</div>", iconSize: [25, 25]}) }).bindPopup('RR# 15 - W7ACS (443.650)<br>').addTo(map);
L.marker([47.7719300000, -122.2810100000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>16</div>", iconSize: [25, 25]}) }).bindPopup('RR# 16 - W7ACS (440.600)<br>').addTo(map);
L.marker([47.5209999100, -122.3430023200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>17</div>", iconSize: [25, 25]}) }).bindPopup('RR# 17 - W7ACS (443.200)<br>').addTo(map);
L.marker([47.6884994500, -122.1559982300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 18 - K7LWH (53.170)<br>RR# 19 - K7LWH (145.490)<br>').addTo(map);
L.marker([47.6814994800, -122.2089996300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 20 - K7LWH (224.360)<br>RR# 21 - K7LWH (441.075)<br>').addTo(map);
L.marker([47.5683670000, -122.2207290000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 22 - W7MIR (147.160)<br>RR# 23 - W7MIR (440.150)<br>').addTo(map);
L.marker([48.5833015400, -122.1449966400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>24</div>", iconSize: [25, 25]}) }).bindPopup('RR# 24 - N7GDE (145.190)<br>').addTo(map);
L.marker([47.6445007300, -122.6949996900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>25</div>", iconSize: [25, 25]}) }).bindPopup('RR# 25 - KC7Z (444.075)<br>').addTo(map);
L.marker([47.6555143000, -122.9594265000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 26 - WW7RA (146.62)<br>RR# 27 - WW7RA (442.65)<br>').addTo(map);
L.marker([48.1170005800, -122.7600021400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>28</div>", iconSize: [25, 25]}) }).bindPopup('RR# 28 - W7JCR (145.150)<br>').addTo(map);
L.marker([48.0583000200, -122.6880035400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>29</div>", iconSize: [25, 25]}) }).bindPopup('RR# 29 - AA7MI (440.725)<br>').addTo(map);
L.marker([47.2150993300, -123.1009979200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 30 - N7SK (146.720)<br>RR# 31 - N7SK (443.250)<br>RR# 32 - N7SK (927.4125)<br>').addTo(map);
L.marker([47.3222999600, -122.3130035400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 33 - WA7FW (146.760)<br>RR# 34 - WA7FW (442.950)<br>').addTo(map);
L.marker([47.2774009700, -122.2919998200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>35</div>", iconSize: [25, 25]}) }).bindPopup('RR# 35 - WA7FW (442.925)<br>').addTo(map);
L.marker([48.0069007900, -122.9710006700], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>36</div>", iconSize: [25, 25]}) }).bindPopup('RR# 36 - KC7EQO (442.100)<br>').addTo(map);
L.marker([47.1997985800, -121.7559967000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>37</div>", iconSize: [25, 25]}) }).bindPopup('RR# 37 - W7AAO (145.370)<br>').addTo(map);
L.marker([46.8431010000, -122.3149560000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 38 - W7EAT (146.700)<br>RR# 40 - W7EAT (442.725)<br>').addTo(map);
L.marker([47.0530272050, -122.2944118600], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 39 - W7EAT (224.180)<br>RR# 75 - N3KPU (145.230)<br>').addTo(map);
L.marker([47.7376770000, -122.2307900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>41</div>", iconSize: [25, 25]}) }).bindPopup('RR# 41 - NE7MC (442.000)<br>').addTo(map);
L.marker([47.5404491400, -122.0989990200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 42 - WW7STR (224.440)<br>RR# 43 - WW7STR (441.550)<br>').addTo(map);
L.marker([47.4884400000, -121.9470500000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>44</div>", iconSize: [25, 25]}) }).bindPopup('RR# 44 - WW7STR (443.050)<br>').addTo(map);
L.marker([47.5559005700, -122.1159973100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>45</div>", iconSize: [25, 25]}) }).bindPopup('RR# 45 - WW7STR (927.2125)<br>').addTo(map);
L.marker([48.5603981000, -123.1200027500], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>46</div>", iconSize: [25, 25]}) }).bindPopup('RR# 46 - N7JN (146.700)<br>').addTo(map);
L.marker([48.6777992200, -122.8310012800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 47 - N7JN (224.480)<br>RR# 48 - N7JN (443.450)<br>').addTo(map);
L.marker([47.2211990400, -121.8509979200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>49</div>", iconSize: [25, 25]}) }).bindPopup('RR# 49 - N7OEP (53.330)<br>').addTo(map);
L.marker([47.2042999300, -121.9919967700], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 50 - N7OEP (440.075)<br>RR# 51 - N7OEP (443.175)<br>').addTo(map);
L.marker([47.7724990800, -122.9300003100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>52</div>", iconSize: [25, 25]}) }).bindPopup('RR# 52 - K7DK (440.950)<br>').addTo(map);
L.marker([46.8672981300, -122.2669982900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 53 - W7PFR (53.410)<br>RR# 54 - W7PFR (443.975)<br>').addTo(map);
L.marker([47.5038986200, -121.9759979200], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 55 - K7NWS (442.075)<br>RR# 56 - K7NWS (145.330)<br>RR# 57 - K7NWS (224.340)<br>').addTo(map);
L.marker([47.3910700000, -122.6079000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>58</div>", iconSize: [25, 25]}) }).bindPopup('RR# 58 - KA7EOC (145.350)<br>').addTo(map);
L.marker([47.9979496000, -122.1944999650], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 59 - WA7LAW (147.180)<br>RR# 60 - WA7LAW (444.575)<br>').addTo(map);
L.marker([47.5301017800, -122.0329971300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>61</div>", iconSize: [25, 25]}) }).bindPopup('RR# 61 - N9VW (53.830)<br>').addTo(map);
L.marker([47.5420280000, -122.1091100000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 62 - KC7RAS (147.100)<br>RR# 63 - N6OBY (443.325)<br>RR# 64 - WA7ACS (440.175)<br>').addTo(map);
L.marker([47.0279998800, -122.8970031700], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>65</div>", iconSize: [25, 25]}) }).bindPopup('RR# 65 - NT7H (147.360)<br>').addTo(map);
L.marker([47.8439700000, -122.5427500000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>68</div>", iconSize: [25, 25]}) }).bindPopup('RR# 68 - NW7DR (444.725)<br>').addTo(map);
L.marker([48.2125015300, -122.7050018300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>69</div>", iconSize: [25, 25]}) }).bindPopup('RR# 69 - W7AVM (146.860)<br>').addTo(map);
L.marker([48.0401001000, -122.4059982300], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>70</div>", iconSize: [25, 25]}) }).bindPopup('RR# 70 - W7AVM (147.220)<br>').addTo(map);
L.marker([47.4508018500, -122.2870025600], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 71 - NC7G (146.660)<br>RR# 72 - WA7ST (443.100)<br>').addTo(map);
L.marker([47.4726950000, -122.3454480000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>73</div>", iconSize: [25, 25]}) }).bindPopup('RR# 73 - W7BUR (441.125)<br>').addTo(map);
L.marker([47.4023300000, -122.3035600000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>74</div>", iconSize: [25, 25]}) }).bindPopup('RR# 74 - WA7DES (443.700)<br>').addTo(map);
L.marker([47.1091003400, -122.5530014000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>76</div>", iconSize: [25, 25]}) }).bindPopup('RR# 76 - KE7YYD (442.750)<br>').addTo(map);
L.marker([47.7542991600, -122.1630020100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 77 - K6RFK (147.340)<br>RR# 78 - K6RFK (442.775)<br>').addTo(map);
L.marker([46.9730987500, -123.1350021400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>79</div>", iconSize: [25, 25]}) }).bindPopup('RR# 79 - K7CPR (145.470)<br>').addTo(map);
L.marker([48.0982722000, -122.5731977000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>80</div>", iconSize: [25, 25]}) }).bindPopup('RR# 80 - N7KN (441.425)<br>').addTo(map);
L.marker([48.2249984700, -122.5000000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 81 - W7PIG (147.360)<br>RR# 83 - W7PIG (441.050)<br>').addTo(map);
L.marker([48.1915016200, -122.5149993900], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>82</div>", iconSize: [25, 25]}) }).bindPopup('RR# 82 - W7PIG (223.880)<br>').addTo(map);
L.marker([47.3125800000, -123.3725683000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>84</div>", iconSize: [25, 25]}) }).bindPopup('RR# 84 - K7CH (53.030)<br>').addTo(map);

</script>
