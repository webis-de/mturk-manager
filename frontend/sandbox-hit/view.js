import {getHeight, getWidth} from '../vue/helpers';

export default class View {
  constructor(loader, controller) {
    this.loader = loader;
    this.controller = controller;
    this.iframe = document.getElementById('iframe');
  }

  update() {
    this.insertTemplate();
    this.resize();
  }

  insertTemplate() {
    const parameters = JSON.parse(this.loader.hit.parameters);

    let { template } = this.loader.hit.batch.settings_batch.template;

    for (const entry of Object.entries(parameters)) {
      template = template.replace(`\${${entry[0]}}`, entry[1]);
    }

    this.iframe.srcdoc = template;
  }

  resize() {
    this.iframe.width = getWidth();
    this.iframe.height = getHeight();
  }
}
