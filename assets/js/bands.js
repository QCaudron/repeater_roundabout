export { readRepeaters, BANDS };
const REPEATERS = "./assets/repeaters.json";
async function readRepeaters() {
    console.log("Fetching data...");
    let response = await fetch(REPEATERS);
    let repeatersRaw = await response.json();
    console.log("Parsing data...");
    let repeaters = repeatersRaw.map((r) => {
        let callsign = r['Callsign'];
        let output = parseFloat(r['Output (MHz)']);
        let offset = parseFloat(r['Offset (MHz)']);
        let input = parseFloat((output + offset).toFixed(4));
        return { callsign, input, output };
    });
    return repeaters;
}
const BANDS = [
    {
        name: "2m",
        extent: [144, 148],
        zones: [
            // {name: 'CW', min: 144.0, max: 144.1, color: 'gray'},
            // {name: 'SSB', min: 144.1, max: 144.275, color: 'darkorange'},
            { name: 'FM Inputs', min: 144.5, max: 144.9, type: 'fmInputBand' },
            { name: 'FM Outputs', min: 145.1, max: 145.49, type: 'fmOutputBand' },
            { name: 'FM Inputs', min: 146.01, max: 146.4, type: 'fmInputBand' },
            { name: 'FM Outputs', min: 146.62, max: 147.38, type: 'fmOutputBand' },
            { name: 'FM Inputs', min: 147.61, max: 147.99, type: 'fmInputBand' },
            { name: 'VNBD Inputs', min: 147.40625, max: 147.50625, type: 'fmInputBand' },
            { name: 'VNBD Outputs', min: 146.40625, max: 146.50625, type: 'fmOutputBand' },
        ],
    },
    {
        name: "6m",
        extent: [50, 54],
        zones: [
            { name: 'FM Inputs', min: 51.1, max: 52.29, type: 'fmInputBand' },
            { name: 'FM Outputs', min: 52.8, max: 53.99, type: 'fmOutputBand' },
        ],
    },
    {
        name: "1.25m",
        extent: [222, 225],
        zones: [
            { name: 'FM Inputs', min: 222.18, max: 222.38, type: 'fmInputBand' },
            { name: 'FM Inputs', min: 222.42, max: 223.02, type: 'fmInputBand' },
            { name: 'FM Inputs', min: 223.08, max: 223.22, type: 'fmInputBand' },
            { name: 'FM Inputs', min: 223.26, max: 223.38, type: 'fmInputBand' },
            { name: 'FM Outputs', min: 223.78, max: 223.98, type: 'fmOutputBand' },
            { name: 'FM Outputs', min: 224.02, max: 224.62, type: 'fmOutputBand' },
            { name: 'FM Outputs', min: 224.68, max: 224.82, type: 'fmOutputBand' },
            { name: 'FM Outputs', min: 224.86, max: 224.98, type: 'fmOutputBand' },
        ],
    },
    {
        name: "70cm",
        extent: [430, 450],
        zones: [
            { name: 'FM Inputs', min: 445.0, max: 450.0, type: 'fmInputBand' },
            { name: 'FM Outputs', min: 440.9125, max: 445.0, type: 'fmOutputBand' },
            { name: 'FM Outputs', min: 440.0, max: 440.7, type: 'fmOutputBand' },
        ],
    }
];
//# sourceMappingURL=bands.js.map