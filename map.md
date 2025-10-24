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
L.marker([47.6238400000, -122.3151900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>2</div>", iconSize: [25, 25]}) }).bindPopup('RR# 2 - WW7PSR (52.870)<br>').addTo(map);
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
L.marker([46.4882000000, -123.2148000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 40 - K7CH (53.030)<br>RR# 43 - K7CH (927.925)<br>RR# 54 - K7CH (444.450)<br>').addTo(map);
L.marker([47.3161550000, -123.3578300000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>41</div>", iconSize: [25, 25]}) }).bindPopup('RR# 41 - K7CH (440.650)<br>').addTo(map);
L.marker([47.3203000000, -122.3386000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>42</div>", iconSize: [25, 25]}) }).bindPopup('RR# 42 - K7CH (927.250)<br>').addTo(map);
L.marker([47.5417445000, -122.1091650000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 44 - N9VW (443.325)<br>RR# 45 - KC7RAS (147.100)<br>').addTo(map);
L.marker([48.2261900000, -122.5019000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>46</div>", iconSize: [25, 25]}) }).bindPopup('RR# 46 - W7PIG (147.360)<br>').addTo(map);
L.marker([48.2247000000, -122.4989000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>47</div>", iconSize: [25, 25]}) }).bindPopup('RR# 47 - W7PIG (223.880)<br>').addTo(map);
L.marker([48.0800000000, -122.3775000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>48</div>", iconSize: [25, 25]}) }).bindPopup('RR# 48 - W7PIG (441.050)<br>').addTo(map);
L.marker([47.6299300000, -121.9500800000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>49</div>", iconSize: [25, 25]}) }).bindPopup('RR# 49 - WA7TBP (223.960)<br>').addTo(map);
L.marker([47.7600000000, -122.3500000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>50</div>", iconSize: [25, 25]}) }).bindPopup('RR# 50 - W7AUX (224.020)<br>').addTo(map);
L.marker([47.7561900000, -122.3457500000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 51 - W7AUX (440.300)<br>RR# 53 - W7AUX (927.638)<br>').addTo(map);
L.marker([47.7680000000, -122.3531000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>52</div>", iconSize: [25, 25]}) }).bindPopup('RR# 52 - W7AUX (442.825)<br>').addTo(map);

</script>
