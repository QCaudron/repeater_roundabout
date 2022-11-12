export { Spectrum };
class Spectrum {
    constructor() {
        console.log("Spectrum");
    }
}
import { Pane } from "https://cdn.skypack.dev/tweakpane@3.1.0";
const REPEATERS = "https://raw.githubusercontent.com/QCaudron/repeater_roundabout/main/assets/repeaters.json";
// Tweakpane parameters
const params = {
    width: 800,
    height: 70,
    background: 'rgb(0, 0, 0)',
    fmBW: 16,
    vnbDigBW: 12.5,
    unbDigBW: 6.25,
    outputColor: 'rgb(0, 0, 255)',
    inputColor: 'rgb(255, 0, 0)',
    outputBandColor: 'rgb(0, 0, 128)',
    inputBandColor: 'rgb(128, 0, 0)',
};
let canvas;
let freq;
let chz;
let repeaters;
const bandMin = 144.0;
const bandMax = 148.0;
const typeColor = new Map();
const twoMeterZones = [
    // {name: 'CW', min: 144.0, max: 144.1, color: 'gray'},
    // {name: 'SSB', min: 144.1, max: 144.275, color: 'darkorange'},
    { name: 'FM Inputs', min: 144.5, max: 144.9, type: 'fmInputBand' },
    { name: 'FM Outputs', min: 145.1, max: 145.49, type: 'fmOutputBand' },
    { name: 'FM Inputs', min: 146.01, max: 146.4, type: 'fmInputBand' },
    { name: 'FM Outputs', min: 146.62, max: 147.38, type: 'fmOutputBand' },
    { name: 'FM Inputs', min: 147.61, max: 147.99, type: 'fmInputBand' },
    { name: 'VNBD Inputs', min: 147.40625, max: 147.50625, type: 'fmInputBand' },
    { name: 'VNBD Outputs', min: 146.40625, max: 146.50625, type: 'fmOutputBand' },
];
function createPane(container) {
    const pane = new Pane({ container });
    // pane.registerPlugin(EssentialsPlugin);
    const fParams = pane.addFolder({ title: 'Params' });
    fParams.addInput(params, 'width', { min: 200, max: 1200, step: 10 });
    fParams.addInput(params, 'height', { min: 30, max: 400, step: 10 });
    fParams.addInput(params, 'fmBW', { min: 1, max: 20, step: 0.5 });
    fParams.addInput(params, 'background', { view: 'color' });
    fParams.addInput(params, 'outputColor', { view: 'color' });
    fParams.addInput(params, 'inputColor', { view: 'color' });
    fParams.addInput(params, 'outputBandColor', { view: 'color' });
    fParams.addInput(params, 'inputBandColor', { view: 'color' });
    pane.on('change', (ev) => {
        refresh();
    });
}
async function main() {
    canvas = document.getElementById("canvas");
    freq = document.getElementById("freq");
    chz = document.getElementById("chz");
    createPane(document.body);
    canvas.addEventListener('mousemove', (e) => {
        let [r, f] = repeaterFromFreq(freqFromX(e.offsetX));
        let displayed = f.toFixed(4);
        freq.innerText = displayed.slice(0, -1);
        chz.innerText = displayed.slice(-1);
        if (r !== null) {
            console.log(r);
        }
    });
    console.log("Fetching data...");
    let response = await fetch(REPEATERS);
    let repeatersRaw = await response.json();
    console.log("Parsing data...");
    repeaters = repeatersRaw.map((r) => {
        let callsign = r['Callsign'];
        let output = parseFloat(r['Output (MHz)']);
        let offset = parseFloat(r['Offset (MHz)']);
        let input = parseFloat((output + offset).toFixed(4));
        return { callsign, input, output };
    });
    refresh();
}
function refresh() {
    canvas.height = params.height;
    canvas.width = params.width;
    for (let elt of document.querySelectorAll('.display')) {
        elt.style.width = `${params.width}px`;
    }
    // Track changes to color pallette
    typeColor.set('fmInputBand', params.inputBandColor);
    typeColor.set('fmOutputBand', params.outputBandColor);
    typeColor.set('fmInput', params.inputColor);
    typeColor.set('fmOutput', params.outputColor);
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = params.background;
    ctx.fillRect(0, 0, params.width, params.height);
    for (let zone of twoMeterZones) {
        drawZone(ctx, zone);
    }
    for (let repeater of repeaters) {
        if (repeater.output < 144 || repeater.output > 148) {
            continue;
        }
        // console.log(`${repeater.callsign}: ${repeater.output} ${repeater.input}`);
        drawZone(ctx, {
            name: repeater.callsign,
            min: repeater.output - params.fmBW / 2 / 1000,
            max: repeater.output + params.fmBW / 2 / 1000,
            type: 'fmOutput'
        });
        drawZone(ctx, {
            name: repeater.callsign,
            min: repeater.input - params.fmBW / 2 / 1000,
            max: repeater.input + params.fmBW / 2 / 1000,
            type: 'fmInput'
        });
    }
}
function drawZone(ctx, zone) {
    const xMin = scaleX(zone.min);
    const xMax = scaleX(zone.max);
    // console.log(`${zone.name}: ${xMin}-${xMax}`);
    ctx.fillStyle = typeColor.get(zone.type);
    ctx.fillRect(xMin, 0, xMax - xMin, params.height);
}
function scaleX(f) {
    return params.width * (f - bandMin) / (bandMax - bandMin);
}
function freqFromX(x) {
    let f = bandMin + (x / params.width) * (bandMax - bandMin);
    return f;
}
function repeaterFromFreq(f) {
    let best = null;
    let distBest = 1000;
    let bestF = 144.0;
    for (let repeater of repeaters) {
        for (let fT of [repeater.input, repeater.output]) {
            if (!best || Math.abs(f - fT) < distBest) {
                best = repeater;
                distBest = Math.abs(f - fT);
                bestF = fT;
                continue;
            }
        }
    }
    if (distBest > params.fmBW / 1000) {
        return [null, f];
    }
    return [best, bestF];
}
main();
//# sourceMappingURL=spectrum.js.map