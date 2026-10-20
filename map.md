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

</script>
