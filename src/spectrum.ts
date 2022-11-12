export { Spectrum, SpectrumOptions, UIParams };

interface SpectrumOptions {
    band: [number, number];
}

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

const REPEATERS = "https://raw.githubusercontent.com/QCaudron/repeater_roundabout/main/assets/repeaters.json";

let canvas: HTMLCanvasElement;
let freq: HTMLElement;
let chz: HTMLElement;
let repeaters: Repeater[];

const bandMin = 144.0;
const bandMax = 148.0;

interface Zone {
  name: string;
  type:
    'fmInputBand' | 'fmOutputBand' |
    'fmInput' | 'fmOutput';
  min: number,
  max: number
}

const typeColor: Map<string, string> = new Map();

interface Repeater {
  callsign: string,
  input: number,
  output: number
}

interface RoundaboutRep {
    "Group Name": string,
    Callsign: string,
    Location: string,
    Mode: string,
    "Output (MHz)": string,
    "Offset (MHz)": string,
    "Tone (Hz)": string,
    Coordinates: [number, number],
    "Long Name": string,
    Website: string,
}

const twoMeterZones: Zone[] = [
  // {name: 'CW', min: 144.0, max: 144.1, color: 'gray'},
  // {name: 'SSB', min: 144.1, max: 144.275, color: 'darkorange'},
  {name: 'FM Inputs', min: 144.5, max: 144.9, type: 'fmInputBand'},
  {name: 'FM Outputs', min: 145.1, max: 145.49, type: 'fmOutputBand'},
  {name: 'FM Inputs', min: 146.01, max: 146.4, type: 'fmInputBand'},
  {name: 'FM Outputs', min: 146.62, max: 147.38, type: 'fmOutputBand'},
  {name: 'FM Inputs', min: 147.61, max: 147.99, type: 'fmInputBand'},
  {name: 'VNBD Inputs', min: 147.40625, max: 147.50625, type: 'fmInputBand'},
  {name: 'VNBD Outputs', min: 146.40625, max: 146.50625, type: 'fmOutputBand'},
];

class Spectrum {
    canvas: HTMLCanvasElement;
    ctx: CanvasRenderingContext2D;
    freq: HTMLSpanElement;
    chz: HTMLSpanElement;
    options: SpectrumOptions;
    params: UIParams;
    repeaters: Repeater[] | undefined;

    constructor(parent: HTMLElement, options: SpectrumOptions, params: UIParams) {
        console.log(`Spectrum ${options}`);
        this.options = options;
        this.params = params;

        parent.insertAdjacentHTML(
            'beforeend',
            `<div class="spectrum-channel">
                <span class="spectrum-freq">${options.band[0]}</span><span class="spectrum-chz">0</span>
            </div>

            <canvas class="spectrum-canvas"></canvas>
            `);

        this.canvas = parent.querySelector(".spectrum-canvas") as HTMLCanvasElement;
        this.ctx = this.canvas.getContext('2d')!;
        this.freq = parent.querySelector('.spectrum-freq') as HTMLSpanElement;
        this.chz = parent.querySelector('.spectrum-chz') as HTMLSpanElement;
        this.init();
    }

    async init() {
        console.log("Fetching data...");
        let response = await fetch(REPEATERS);
        let repeatersRaw = await response.json();
        console.log("Parsing data...");
        this.repeaters = repeatersRaw.map((r: RoundaboutRep) => {
            let callsign = r['Callsign'];
            let output = parseFloat(r['Output (MHz)']);
            let offset = parseFloat(r['Offset (MHz)']);
            let input = parseFloat((output + offset).toFixed(4));
            return { callsign, input, output };
        });

        this.refresh();

        this.canvas.addEventListener('mousemove', (e) => {
            let [r, f] = repeaterFromFreq(
                this.freqFromX(e.offsetX),
                this.params.fmBW,
                this.repeaters!);
            let displayed = f.toFixed(4);
            this.freq.innerText = displayed.slice(0, -1);
            this.chz.innerText = displayed.slice(-1);
            if (r !== null) {
                console.log(r);
            }
        });
    }

    refresh() {
        this.canvas.height = this.params.height;
        this.canvas.width = this.params.width;
        for (let elt of document.querySelectorAll('.spectrum-channel') as NodeListOf<HTMLElement>) {
          elt.style.width = `${this.params.width}px`;
        }

        // Track changes to color pallette
        typeColor.set('fmInputBand', this.params.inputBandColor);
        typeColor.set('fmOutputBand', this.params.outputBandColor);
        typeColor.set('fmInput', this.params.inputColor);
        typeColor.set('fmOutput', this.params.outputColor);

        this.ctx.fillStyle = this.params.background;
        this.ctx.fillRect(0, 0, this.params.width, this.params.height);

        for (let zone of twoMeterZones) {
          this.drawZone(zone);
        }

        for (let repeater of this.repeaters!) {
          if (repeater.output < 144 || repeater.output > 148) {
            continue;
          }
          // console.log(`${repeater.callsign}: ${repeater.output} ${repeater.input}`);
          this.drawZone({
            name: repeater.callsign,
            min: repeater.output - this.params.fmBW/2/1000,
            max: repeater.output + this.params.fmBW/2/1000,
            type: 'fmOutput'
          });
          this.drawZone({
            name: repeater.callsign,
            min: repeater.input - this.params.fmBW/2/1000,
            max: repeater.input + this.params.fmBW/2/1000,
            type: 'fmInput'
          });
        }
      }

      drawZone(zone: Zone) {
        const xMin = this.scaleX(zone.min);
        const xMax = this.scaleX(zone.max);
        // console.log(`${zone.name}: ${xMin}-${xMax}`);
        this.ctx.fillStyle = typeColor.get(zone.type)!;
        this.ctx.fillRect(xMin, 0, xMax - xMin, this.params.height);
      }

      scaleX(f: number): number {
        let [bandMin, bandMax] = this.options.band;
        return this.params.width * (f - bandMin) / (bandMax - bandMin);
      }

      freqFromX(x: number): number {
        let [bandMin, bandMax] = this.options.band;
        let f = bandMin + (x / this.params.width) * (bandMax - bandMin);
        return f;
      }
}

function repeaterFromFreq(f: number, kHzSlop: number, repeaters: Repeater[]): [Repeater | null, number] {
    let best: Repeater | null = null;
    let distBest: number = 1000;
    let bestF: number = 144.0;

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

    if (distBest > kHzSlop/1000) {
      return [null, f];
    }

    return [best, bestF];
  }
