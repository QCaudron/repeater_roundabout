export { Spectrum };
;
let canvas;
let freq;
let chz;
let repeaters;
const bandMin = 144.0;
const bandMax = 148.0;
const typeColor = new Map();
class Spectrum {
    constructor(repeaters, band, parent, params) {
        console.log(`Spectrum ${band.name}`);
        this.repeaters = repeaters;
        this.band = band;
        this.params = params;
        parent.insertAdjacentHTML('beforeend', `<div class="channel">
                <span class="freq">${band.extent[0]}</span><span class="chz">0</span>
            </div>

            <canvas></canvas>
            `);
        this.canvas = parent.querySelector("canvas");
        this.ctx = this.canvas.getContext('2d');
        this.channel = parent.querySelector("div.channel");
        this.freq = parent.querySelector('span.freq');
        this.chz = parent.querySelector('span.chz');
        this.init();
    }
    init() {
        this.refresh();
        this.updateChannel(this.band.extent[0]);
        this.canvas.addEventListener('mousemove', (e) => {
            this.updateChannel(this.freqFromX(e.offsetX));
        });
    }
    refresh() {
        this.canvas.height = this.params.height;
        this.canvas.width = this.params.width;
        this.channel.style.width = `${this.params.width}px`;
        // Track changes to color pallette
        typeColor.set('fmInputBand', this.params.inputBandColor);
        typeColor.set('fmOutputBand', this.params.outputBandColor);
        typeColor.set('fmInput', this.params.inputColor);
        typeColor.set('fmOutput', this.params.outputColor);
        this.ctx.fillStyle = this.params.background;
        this.ctx.fillRect(0, 0, this.params.width, this.params.height);
        for (let zone of this.band.zones) {
            this.drawZone(zone);
        }
        let [bandMin, bandMax] = this.band.extent;
        for (let repeater of this.repeaters) {
            if (repeater.output < bandMin || repeater.output > bandMax) {
                continue;
            }
            // console.log(`${repeater.callsign}: ${repeater.output} ${repeater.input}`);
            this.drawZone({
                name: repeater.callsign,
                min: repeater.output - this.params.fmBW / 2 / 1000,
                max: repeater.output + this.params.fmBW / 2 / 1000,
                type: 'fmOutput'
            });
            this.drawZone({
                name: repeater.callsign,
                min: repeater.input - this.params.fmBW / 2 / 1000,
                max: repeater.input + this.params.fmBW / 2 / 1000,
                type: 'fmInput'
            });
        }
    }
    updateChannel(freq) {
        let [r, f] = repeaterFromFreq(freq, this.params.fmBW, this.repeaters);
        let displayed = f.toFixed(4);
        this.freq.innerText = displayed.slice(0, -1);
        this.chz.innerText = displayed.slice(-1);
        if (r !== null) {
            console.log(r);
        }
    }
    drawZone(zone) {
        const xMin = this.scaleX(zone.min);
        const xMax = this.scaleX(zone.max);
        // console.log(`${zone.name}: ${xMin}-${xMax}`);
        this.ctx.fillStyle = typeColor.get(zone.type);
        this.ctx.fillRect(xMin, 0, xMax - xMin, this.params.height);
    }
    scaleX(f) {
        let [bandMin, bandMax] = this.band.extent;
        return this.params.width * (f - bandMin) / (bandMax - bandMin);
    }
    freqFromX(x) {
        let [bandMin, bandMax] = this.band.extent;
        let f = bandMin + (x / this.params.width) * (bandMax - bandMin);
        return f;
    }
}
function repeaterFromFreq(f, kHzSlop, repeaters) {
    let best = null;
    let distBest = 1000;
    let bestF = 0;
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
    if (distBest > kHzSlop / 1000) {
        return [null, f];
    }
    return [best, bestF];
}
//# sourceMappingURL=spectrum.js.map