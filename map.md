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

L.marker([47.6395000000, -122.3693000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>1</div>", iconSize: [25, 25]}) }).bindPopup('RR# 1 - WW7PSR (146.9600)<br>').addTo(map);
L.marker([47.6238400000, -122.3151900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>2</div>", iconSize: [25, 25]}) }).bindPopup('RR# 2 - WW7PSR (52.8700)<br>').addTo(map);
L.marker([46.5139007600, -121.2080001800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>3</div>", iconSize: [25, 25]}) }).bindPopup('RR# 3 - WA7SAR (146.860)<br>').addTo(map);
L.marker([46.0633010900, -121.4240036000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>4</div>", iconSize: [25, 25]}) }).bindPopup('RR# 4 - WA7SAR (147.080)<br>').addTo(map);
L.marker([46.5222015400, -120.3330001800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>5</div>", iconSize: [25, 25]}) }).bindPopup('RR# 5 - WA7SAR (444.600)<br>').addTo(map);
L.marker([47.5087500000, -121.9851900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 6 - K7NWS (145.3300)<br>RR# 7 - K7NWS (224.3400)<br>').addTo(map);
L.marker([47.5100000000, -121.9900000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>8</div>", iconSize: [25, 25]}) }).bindPopup('RR# 8 - K7NWS (442.0750)<br>').addTo(map);
L.marker([47.7253000000, -122.1189000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>9</div>", iconSize: [25, 25]}) }).bindPopup('RR# 9 - K6RFK (147.3400)<br>').addTo(map);
L.marker([47.7433000000, -122.1259000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>10</div>", iconSize: [25, 25]}) }).bindPopup('RR# 10 - K6RFK (442.7750)<br>').addTo(map);
L.marker([47.2193600000, -121.8422566667], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 11 - N7OEP (440.0750)<br>RR# 12 - N7OEP (443.1750)<br>RR# 13 - N7OEP (53.3300)<br>').addTo(map);
L.marker([47.5683800000, -122.2207800000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 14 - W7MIR (147.1600)<br>RR# 15 - W7MIR (440.1500)<br>').addTo(map);
L.marker([47.7500000000, -124.1766600000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>16</div>", iconSize: [25, 25]}) }).bindPopup('RR# 16 - K7PP (147.2800)<br>').addTo(map);
L.marker([47.5491670000, -122.7838800000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>17</div>", iconSize: [25, 25]}) }).bindPopup('RR# 17 - K7PP (441.2000)<br>').addTo(map);
L.marker([46.4614300000, -123.5462000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>18</div>", iconSize: [25, 25]}) }).bindPopup('RR# 18 - K7PP (441.3000)<br>').addTo(map);
L.marker([47.5414000000, -122.1092000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>19</div>", iconSize: [25, 25]}) }).bindPopup('RR# 19 - K7PP (443.4000)<br>').addTo(map);
L.marker([43.9760707000, -116.4075535000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 20 - K7SWI (224.940)<br>RR# 21 - K7SWI (444.375)<br>RR# 22 - N7UBO (146.740)<br>').addTo(map);
L.marker([43.4109190000, -116.5895690000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>23</div>", iconSize: [25, 25]}) }).bindPopup('RR# 23 - KI7PWR (146.920)<br>').addTo(map);
L.marker([47.4880500000, -121.9469400000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 24 - K7LED (146.8200)<br>RR# 25 - K7LED (224.1200)<br>').addTo(map);
L.marker([46.9965144000, -120.5478474000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>26</div>", iconSize: [25, 25]}) }).bindPopup('RR# 26 - WA7SAR (145.270)<br>').addTo(map);
L.marker([47.6745900000, -122.0539300000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>27</div>", iconSize: [25, 25]}) }).bindPopup('RR# 27 - W7DX (147.0000)<br>').addTo(map);
L.marker([46.8354000000, -122.2878000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>...</div>", iconSize: [25, 25]}) }).bindPopup('RR# 28 - W7PFR (53.4100)<br>RR# 29 - W7PFR (443.9750)<br>').addTo(map);
L.marker([47.5544700000, -122.1323900000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>30</div>", iconSize: [25, 25]}) }).bindPopup('RR# 30 - K7BEL (441.1000)<br>').addTo(map);
L.marker([46.5929985000, -120.5380020100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>31</div>", iconSize: [25, 25]}) }).bindPopup('RR# 31 - WA7SAR (147.060)<br>').addTo(map);
L.marker([45.9937300000, -118.1805300000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>32</div>", iconSize: [25, 25]}) }).bindPopup('RR# 32 - KB7ARA (147.280)<br>').addTo(map);
L.marker([46.7323989900, -117.0000000000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>33</div>", iconSize: [25, 25]}) }).bindPopup('RR# 33 - KA7FVV (147.320)<br>').addTo(map);
L.marker([48.1813900000, -117.9891700000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>34</div>", iconSize: [25, 25]}) }).bindPopup('RR# 34 - N7WRR (147.360)<br>').addTo(map);
L.marker([47.5749500000, -117.0811300000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>35</div>", iconSize: [25, 25]}) }).bindPopup('RR# 35 - N7WRQ (147.380)<br>').addTo(map);
L.marker([46.0038986200, -112.5339965800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>36</div>", iconSize: [25, 25]}) }).bindPopup('RR# 36 - KB7ARA (147.020)<br>').addTo(map);
L.marker([45.7415084800, -121.6861877400], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>37</div>", iconSize: [25, 25]}) }).bindPopup('RR# 37 - W6TQF (440.325)<br>').addTo(map);
L.marker([47.3819999700, -122.2269973800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>38</div>", iconSize: [25, 25]}) }).bindPopup('RR# 38 - K7CST (147.3200)<br>').addTo(map);
L.marker([48.5947460000, -122.1594200000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>39</div>", iconSize: [25, 25]}) }).bindPopup('RR# 39 - N7GDE (145.1900)<br>').addTo(map);
L.marker([46.6305999800, -120.5350036600], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>40</div>", iconSize: [25, 25]}) }).bindPopup('RR# 40 - N7YRC (444.750)<br>').addTo(map);
L.marker([46.6268005400, -120.7389984100], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>41</div>", iconSize: [25, 25]}) }).bindPopup('RR# 41 - N7YRC (442.725)<br>').addTo(map);
L.marker([46.6539993300, -120.5299987800], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>42</div>", iconSize: [25, 25]}) }).bindPopup('RR# 42 - KC7VQR (147.240)<br>').addTo(map);
L.marker([47.7597700000, -122.5176400000], {icon: L.divIcon({className: 'custom-icon', html: "<div class='icon-label'>43</div>", iconSize: [25, 25]}) }).bindPopup('RR# 43 - KJ7GWR (440.5750)<br>').addTo(map);

</script>
