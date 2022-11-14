export { Spectrum };
;
// Pixel precision for hovering over frequency.
const SLOP = 5;
const typeColor = new Map();
class Spectrum {
    constructor(repeaters, band, parent, params) {
        console.log(`Spectrum ${band.name}`);
        this.repeaters = repeaters;
        this.band = band;
        this.cursor = band.extent[0];
        this.params = params;
        parent.insertAdjacentHTML('beforeend', `<div class="spectrum">
              <div class="info"></div>
              <div class="org"></div>
              <div class="channel">
                  <span class="freq">${band.extent[0]}</span><span class="chz">0</span>
              </div>
              <canvas></canvas>
            </div>`);
        this.outer = parent.lastChild;
        this.canvas = this.outer.querySelector("canvas");
        this.ctx = this.canvas.getContext('2d');
        this.info = this.outer.querySelector("div.info");
        this.org = this.outer.querySelector("div.org");
        this.freq = this.outer.querySelector('span.freq');
        this.chz = this.outer.querySelector('span.chz');
        this.refresh();
        this.updateChannel(this.band.extent[0]);
        this.canvas.addEventListener('mousemove', (e) => {
            this.updateChannel(this.freqFromX(e.offsetX));
        });
    }
    refresh() {
        this.canvas.height = this.params.height;
        this.canvas.width = this.params.width;
        this.outer.style.width = `${this.params.width}px`;
        // Track changes to color pallette
        typeColor.set('fmInputBand', this.params.inputBandColor);
        typeColor.set('fmOutputBand', this.params.outputBandColor);
        typeColor.set('fmInput', this.params.inputColor);
        typeColor.set('fmOutput', this.params.outputColor);
        typeColor.set('cursor', 'greenyellow');
        this.draw();
    }
    draw() {
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
        this.drawZone({
            name: '',
            min: this.cursor, max: this.cursor,
            type: 'cursor'
        });
    }
    updateChannel(freq) {
        let [r, f] = this.repeaterFromFreq(freq);
        let displayed = f.toFixed(4);
        this.freq.innerText = displayed.slice(0, -1);
        this.chz.innerText = displayed.slice(-1);
        if (r !== null) {
            this.info.innerHTML =
                `${r.callsign}` +
                    `<br><span class="output">output: ${smartRound(r.output, 3, 4)}</span>` +
                    `<br><span class="input">input: ${smartRound(r.input, 3, 4)}</span>` +
                    `<br><span class="tone">tone: ${r.tone}</span>`;
            this.org.innerHTML = `${r.org}`;
        }
        else {
            this.info.innerText = '';
            this.org.innerText = '';
        }
        this.cursor = f;
        this.draw();
    }
    drawZone(zone) {
        let xMin = this.scaleX(zone.min);
        let xMax = this.scaleX(zone.max);
        // At least one unit of width
        if (xMax - xMin < 1) {
            xMin = (xMax + xMin) / 2 - 0.5;
            xMax = xMin + 1;
        }
        if (zone.type == 'cursor') {
            this.ctx.strokeStyle = typeColor.get(zone.type);
            this.ctx.setLineDash([5, 5]);
            this.ctx.beginPath();
            this.ctx.moveTo((xMin + xMax) / 2, 0);
            this.ctx.lineTo((xMin + xMax) / 2, this.params.height);
            this.ctx.stroke();
        }
        else {
            this.ctx.fillStyle = typeColor.get(zone.type);
            this.ctx.fillRect(xMin, 0, xMax - xMin, this.params.height);
        }
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
    repeaterFromFreq(f) {
        let best = null;
        let distBest = 1000;
        let bestF = 0;
        for (let repeater of this.repeaters) {
            for (let fT of [repeater.input, repeater.output]) {
                if (!best || Math.abs(f - fT) < distBest) {
                    best = repeater;
                    distBest = Math.abs(f - fT);
                    bestF = fT;
                    continue;
                }
            }
        }
        if (Math.abs(this.scaleX(f) - this.scaleX(bestF)) > SLOP) {
            return [null, f];
        }
        return [best, bestF];
    }
}
function smartRound(n, minDigits, maxDigits) {
    let digits = maxDigits;
    let result = n.toFixed(maxDigits);
    while (digits > minDigits && result.endsWith('0')) {
        digits--;
        result = n.toFixed(digits);
    }
    return result;
}
//# sourceMappingURL=spectrum.js.map