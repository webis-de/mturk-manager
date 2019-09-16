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
    this.iframe.width = this.getWidth();
    this.iframe.height = this.getHeight();
  }

  getWidth() {
    return Math.max(
      document.body.scrollWidth,
      document.documentElement.scrollWidth,
      document.body.offsetWidth,
      document.documentElement.offsetWidth,
      document.documentElement.clientWidth,
    );
  }

  getHeight() {
    return Math.max(
      document.body.scrollHeight,
      document.documentElement.scrollHeight,
      document.body.offsetHeight,
      document.documentElement.offsetHeight,
      document.documentElement.clientHeight,
    );
  }
}
