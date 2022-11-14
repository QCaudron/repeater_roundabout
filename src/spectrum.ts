export { Spectrum, UIParams, Band, Zone };

interface UIParams {
    width: number,
    height: number,
    background: string,      // color
    fmBW: number,            // kHz
    vnbDigBW: number,        // DMR kHz
    unbDigBW: number,        // DStar kHz
    outputColor: string,     // color
    inputColor: string,      // color
    outputBandColor: string, // color
    inputBandColor: string,  // color
};

// Pixel precision for hovering over frequency.
const SLOP = 5;

interface Zone {
    name: string;
    type:
    'fmInputBand' | 'fmOutputBand' | 'fmInput' | 'fmOutput' | 'cursor';
    min: number,
    max: number
}

const typeColor: Map<string, string> = new Map();

interface Repeater {
    callsign: string,
    input: number,
    output: number,
    tone: string,
    org: string
}

interface Band {
    name: string,
    extent: [number, number],
    zones: Zone[],
}

class Spectrum {
    outer: HTMLDivElement;
    canvas: HTMLCanvasElement;
    ctx: CanvasRenderingContext2D;
    info: HTMLDivElement;
    org: HTMLDivElement;
    freq: HTMLSpanElement;
    chz: HTMLSpanElement;
    cursor: number;
    band: Band;
    params: UIParams;
    repeaters: Repeater[];

    constructor(
        repeaters: Repeater[],
        band: Band,
        params: UIParams) {
        console.log(`Spectrum ${band.name}`);
        this.repeaters = repeaters;
        this.band = band;
        this.cursor = band.extent[0];
        this.params = params;

        this.outer = document.createElement('div');
        this.outer.className = 'spectrum';
        this.outer.innerHTML =
            `<div class="spectrum">
              <div class="info"></div>
              <div class="org"></div>
              <div class="channel">
                  <span class="freq">${band.extent[0]}</span><span class="chz">0</span>
              </div>
              <canvas></canvas>
            </div>`;


        this.canvas = this.outer.querySelector("canvas") as HTMLCanvasElement;
        this.ctx = this.canvas.getContext('2d')!;

        this.info = this.outer.querySelector("div.info") as HTMLDivElement;
        this.org = this.outer.querySelector("div.org") as HTMLDivElement;
        this.freq = this.outer.querySelector('span.freq') as HTMLSpanElement;
        this.chz = this.outer.querySelector('span.chz') as HTMLSpanElement;

        this.refresh();
        this.updateChannel(this.band.extent[0]);

        this.canvas.addEventListener('mousemove', (e) => {
            // Scale x coordinate according to browser window scaling.
            let x = e.offsetX / this.canvas.offsetWidth * this.params.width;
            this.updateChannel(this.freqFromX(x));
        });
    }

    refresh() {
        this.canvas.height = this.params.height;
        this.canvas.width = this.params.width;

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

    updateChannel(freq: number) {
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
        } else {
            this.info.innerText = '';
            this.org.innerText = '';
        }

        this.cursor = f;
        this.draw();
    }

    drawZone(zone: Zone) {
        let xMin = this.scaleX(zone.min);
        let xMax = this.scaleX(zone.max);
        // At least one unit of width
        if (xMax - xMin < 1) {
            xMin = (xMax + xMin) / 2 - 0.5;
            xMax = xMin + 1;
        }

        if (zone.type == 'cursor') {
            this.ctx.strokeStyle = typeColor.get(zone.type)!;
            this.ctx.setLineDash([5, 5]);
            this.ctx.beginPath();
            this.ctx.moveTo((xMin + xMax)/2, 0);
            this.ctx.lineTo((xMin + xMax)/2, this.params.height);
            this.ctx.stroke();
        } else {
            this.ctx.fillStyle = typeColor.get(zone.type)!;
            this.ctx.fillRect(xMin, 0, xMax - xMin, this.params.height);
        }
    }

    scaleX(f: number): number {
        let [bandMin, bandMax] = this.band.extent;
        return this.params.width * (f - bandMin) / (bandMax - bandMin);
    }

    freqFromX(x: number): number {
        let [bandMin, bandMax] = this.band.extent;
        let f = bandMin + (x / this.params.width) * (bandMax - bandMin);
        return f;
    }

    repeaterFromFreq(f: number): [Repeater | null, number] {
        let best: Repeater | null = null;
        let distBest: number = 1000;
        let bestF: number = 0;

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

function smartRound(n: number, minDigits: number, maxDigits: number) {
    let digits = maxDigits;
    let result = n.toFixed(maxDigits);
    while (digits > minDigits && result.endsWith('0')) {
        digits--;
        result = n.toFixed(digits);
    }
    return result;
}
