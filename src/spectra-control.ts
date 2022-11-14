import { Spectrum } from './spectrum.js';
import { Tabs } from './tabs.js';
import { params } from './spectrum-customizer.js';

import { readRepeaters, BANDS } from './bands.js';

let repeaters = await readRepeaters();

let spectraContainer = document.getElementById('spectra') as HTMLElement;
const tabs = new Tabs(spectraContainer);

for (let band of BANDS) {
    let s = new Spectrum(repeaters, band, params);
    tabs.addTab(band.name, s.outer);
}

tabs.injectContent();

// Default to 2meter band
tabs.select(1);
