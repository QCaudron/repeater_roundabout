
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.2/dist/leaflet.css"
    integrity="sha256-sA+zWATbFveLLNqWO2gtiw3HL/lh1giY/Inf1BJ0z14=" crossorigin="" />
<script src="https://unpkg.com/leaflet@1.9.2/dist/leaflet.js"
    integrity="sha256-o9N1jGDZrf5tS+Ft4gbIK7mYMipq9lqpVJ91xHSyKhg=" crossorigin=""></script>
<style>
    #map {
        height: 600px;
        width: 100%;
    }

    .icon-label {
        background-color: blue;
        color: white;
        text-align: center;
        border-radius: 50%;
        line-height: 25px;
        font-weight: bold;
        width: 25px;
        height: 25px;
    }

    #controls {
        text-align: center;
        margin: 20px;
    }

    .input-group {
        display: inline-block;
        margin: 0 10px;
    }

    #controls label {
        display: block;
        margin-bottom: 5px;
    }

    input {
        width: 80px;
        padding: 5px;
    }

    button {
        margin-left: 10px;
        padding: 5px 10px;
    }

    #input-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
    }
</style>

<div id="controls">
    <div id="input-container">
        <div class="input-group">
            <label for="latitude">Latitude</label>
            <input type="text" id="latitude" value="37.7749">
        </div>
        <div class="input-group">
            <label for="longitude">Longitude</label>
            <input type="text" id="longitude" value="-122.4194">
        </div>
        <div class="input-group">
            <label for="maxDistance">Max Distance (miles)</label>
            <input type="text" id="maxDistance" value="100">
        </div>
        <button id="plotButton">Plot Points</button>
    </div>
</div>

<div id="map"></div>

<script>
    // Leaflet map setup
    var map = L.map('map').setView([47.5, -119.67], 7);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    // Helper function to convert degrees to radians
    function toRadians(degrees) {
        return degrees * (Math.PI / 180);
    }

    // Haversine Formula to calculate the distance between two lat/long points (returns in miles)
    function getDistanceFromLatLon(lat1, lon1, lat2, lon2) {
        const R = 3958.8; // Radius of the earth in miles
        const dLat = toRadians(lat2 - lat1);
        const dLon = toRadians(lon2 - lon1);
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c; // Distance in miles
    }

    // Fetch the CSV data
    async function fetchCSVData() {
        const response = await fetch('https://raw.githubusercontent.com/QCaudron/repeater_roundabout/refs/heads/main/assets/programming_files/all_rr_frequencies.csv');
        const csvText = await response.text();
        return csvText;
    }

    // Parse the CSV data
    function parseCSV(csv) {
        const rows = csv.split('\n').slice(1); // Skip the header row
        const points = rows.map((row, index) => {
            const cols = row.split(',');
            return {
                index: index + 1, // Add 1 because index is zero-based
                callsign: cols[1],
                lat: parseFloat(cols[9]),
                lon: parseFloat(cols[10]),
                freq: cols[2]  // For displaying frequency in the popup
            };
        }).filter(point => !isNaN(point.lat) && !isNaN(point.lon)); // Filter out invalid rows
        return points;
    }

    // Add points to the map
    function addPointsToMap(points, myLocation, maxDistance) {
        points = points.filter(point => {
            const distance = getDistanceFromLatLon(myLocation.lat, myLocation.lon, point.lat, point.lon);
            return distance <= maxDistance;
        });

        // Add markers to the map
        points.forEach(point => {
            const marker = L.marker([point.lat, point.lon], {
                icon: L.divIcon({
                    className: 'custom-icon',
                    html: `<div class='icon-label'>${point.index}</div>`,
                    iconSize: [25, 25]
                })
            }).bindPopup(`RR# ${point.index} - ${point.callsign} (${point.freq} MHz)`);
            marker.addTo(map);
        });
    }

    // Plot points on button click
    document.getElementById('plotButton').addEventListener('click', () => {
        const latitude = parseFloat(document.getElementById('latitude').value);
        const longitude = parseFloat(document.getElementById('longitude').value);
        const maxDistance = parseFloat(document.getElementById('maxDistance').value);

        if (!isNaN(latitude) && !isNaN(longitude) && !isNaN(maxDistance)) {
            fetchCSVData().then(csvText => {
                const points = parseCSV(csvText);
                const myLocation = { lat: latitude, lon: longitude };
                addPointsToMap(points, myLocation, maxDistance);
            });
        } else {
            alert('Please enter valid latitude, longitude, and max distance.');
        }
    });
</script>
