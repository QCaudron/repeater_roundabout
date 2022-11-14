import { Spectrum } from './spectrum.js';
import { Tabs } from './tabs.js';
import { params } from './spectrum-customizer.js';
import { readRepeaters, BANDS } from './bands.js';
let repeaters = await readRepeaters();
let spectraContainer = document.getElementById('spectra');
const tabs = new Tabs(spectraContainer);
for (let band of BANDS) {
    let s = new Spectrum(repeaters, band, params);
    tabs.addTab(band.name, s.outer);
}
tabs.injectContent();
//# sourceMappingURL=spectra-control.js.map