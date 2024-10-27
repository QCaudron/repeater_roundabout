
<style>
    canvas {
        border-radius: 50%; /* Make the canvas appear circular */
        border: 1px solid black;
        display: block;
        margin: 20px auto;
        position: relative;
    }
    #tooltip {
        position: absolute;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 5px;
        display: none;
        border-radius: 5px;
        pointer-events: none;
    }
    #controls {
        text-align: center;
        margin: 20px;
    }
    .input-group {
        display: inline-block;
        margin: 0 10px;
        vertical-align: top;
    }
    #controls label {
        display: block;
        margin-bottom: 5px;
    }
    input {
        width: 80px; /* Narrower input fields */
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
        gap: 15px; /* Space between inputs */
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

<canvas id="azimuthMap" width="500" height="500"></canvas>
<div id="tooltip"></div>

<script>
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

    // Function to calculate the azimuth angle between two points
    function getAzimuth(lat1, lon1, lat2, lon2) {
        const dLon = toRadians(lon2 - lon1);
        const y = Math.sin(dLon) * Math.cos(toRadians(lat2));
        const x = Math.cos(toRadians(lat1)) * Math.sin(toRadians(lat2)) -
            Math.sin(toRadians(lat1)) * Math.cos(toRadians(lat2)) * Math.cos(dLon);
        let theta = Math.atan2(y, x) * 180 / Math.PI; // Angle in degrees

        // Adjust the azimuth so that North is at the top
        theta = (theta - 90 + 360) % 360;  // Subtract 90 degrees and ensure the value is between 0 and 360

        return theta; // Return the adjusted azimuth
    }

    const canvas = document.getElementById('azimuthMap');
    const ctx = canvas.getContext('2d');
    const tooltip = document.getElementById('tooltip');
    const originX = canvas.width / 2;
    const originY = canvas.height / 2;

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
                lon: parseFloat(cols[10])
            };
        }).filter(point => !isNaN(point.lat) && !isNaN(point.lon)); // Filter out invalid rows
        return points;
    }

    // Draw a circular map with points
    function drawMap(points, myLocation, maxDistance) {
        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw the circular boundary
        ctx.beginPath();
        ctx.arc(originX, originY, Math.min(canvas.width, canvas.height) / 2 - 20, 0, 2 * Math.PI);
        ctx.strokeStyle = 'black';
        ctx.stroke();
        ctx.closePath();

        // Filter points based on max distance
        points = points.filter(point => {
            const distance = getDistanceFromLatLon(myLocation.lat, myLocation.lon, point.lat, point.lon);
            return distance <= maxDistance;
        });

        // Find the maximum distance for scaling
        let maxDistanceFound = 0;
        points.forEach(point => {
            const distance = getDistanceFromLatLon(myLocation.lat, myLocation.lon, point.lat, point.lon);
            if (distance > maxDistanceFound) {
                maxDistanceFound = distance;
            }
        });

        const maxCanvasRadius = Math.min(canvas.width, canvas.height) / 2 - 20; // Subtract padding
        const scale = maxCanvasRadius / maxDistanceFound;

        // Draw the points
        points.forEach(point => {
            const distance = getDistanceFromLatLon(myLocation.lat, myLocation.lon, point.lat, point.lon);
            const azimuth = getAzimuth(myLocation.lat, myLocation.lon, point.lat, point.lon);

            // Convert polar to Cartesian coordinates
            const x = originX + distance * scale * Math.cos(toRadians(azimuth));
            const y = originY + distance * scale * Math.sin(toRadians(azimuth));

            point.x = x; // Store x position for hover detection
            point.y = y; // Store y position for hover detection

            // Draw point
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, 2 * Math.PI);
            ctx.fillStyle = 'blue';
            ctx.fill();
            ctx.closePath();
        });
    }

    // Event listener for mouse hover to show tooltip
    canvas.addEventListener('mousemove', (event) => {
        const rect = canvas.getBoundingClientRect();
        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;

        let hovering = false;
        points.forEach(point => {
            const dist = Math.sqrt(Math.pow(mouseX - point.x, 2) + Math.pow(mouseY - point.y, 2));
            if (dist < 5) {
                tooltip.style.left = `${event.clientX}px`; // Align tooltip horizontally with mouse
                tooltip.style.top = `${event.clientY}px`;  // Align tooltip vertically with mouse
                tooltip.innerHTML = `${point.callsign} (RR# ${point.index})`;
                tooltip.style.display = 'block';
                hovering = true;
            }
        });

        if (!hovering) {
            tooltip.style.display = 'none';
        }
    });

    // Fetch the CSV data and plot the map on button click
    let points = [];
    document.getElementById('plotButton').addEventListener('click', () => {
        const latitude = parseFloat(document.getElementById('latitude').value);
        const longitude = parseFloat(document.getElementById('longitude').value);
        const maxDistance = parseFloat(document.getElementById('maxDistance').value);

        if (!isNaN(latitude) && !isNaN(longitude) && !isNaN(maxDistance)) {
            fetchCSVData().then(csvText => {
                points = parseCSV(csvText);
                const myLocation = { lat: latitude, lon: longitude };
                drawMap(points, myLocation, maxDistance);
            });
        } else {
            alert('Please enter valid latitude, longitude, and max distance.');
        }
    });
</script>