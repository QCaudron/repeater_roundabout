import { Pane } from "https://cdn.skypack.dev/tweakpane@3.1.0";
export { Customizer };
// Tweakpane parameters
const params = {
    width: 900,
    height: 80,
    background: 'rgb(0, 0, 0)',
    fmBW: 16,
    vnbDigBW: 12.5,
    unbDigBW: 6.25,
    outputColor: 'rgb(0, 0, 255)',
    inputColor: 'rgb(255, 0, 0)',
    outputBandColor: 'rgb(0, 0, 128)',
    inputBandColor: 'rgb(128, 0, 0)',
};
// Singleton as implemented!
class Customizer {
    constructor(container) {
        this.pane = new Pane({ container });
        this.params = params;
        const fParams = this.pane.addFolder({ title: 'Params' });
        // fParams.addInput(params, 'width', { min: 200, max: 1200, step: 10 });
        fParams.addInput(params, 'height', { min: 30, max: 400, step: 10 });
        fParams.addInput(params, 'fmBW', { min: 1, max: 20, step: 0.5 });
        fParams.addInput(params, 'background', { view: 'color' });
        fParams.addInput(params, 'outputColor', { view: 'color' });
        fParams.addInput(params, 'inputColor', { view: 'color' });
        fParams.addInput(params, 'outputBandColor', { view: 'color' });
        fParams.addInput(params, 'inputBandColor', { view: 'color' });
    }
    on(callback) {
        this.pane.on('change', callback);
    }
}
//# sourceMappingURL=spectrum-customizer.js.map