import Loader from './loader';
import View from './view';

export default class Controller {
  constructor() {
    this.loader = new Loader(this);
    this.view = new View(this.loader, this);
  }

  async init() {
    this.initEvents();
    await this.loader.init();
    await this.loader.syncData();
    this.view.update();
  }

  initEvents() {

  }
}
