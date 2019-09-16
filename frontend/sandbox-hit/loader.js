import localforage from 'localforage';
import axios from 'axios';

export default class Loader {
  constructor() {
    this.slug_project = null;
    this.id_hit = null;
    this.url_api = null;
    this.token_instance = null;
    this.axios = null;
    this.hit = null;
  }

  async init() {
    this.slug_project = new URL(location.href).searchParams.get('slug_project');
    this.id_hit = new URL(location.href).searchParams.get('id_hit');
    this.url_api = await localforage.getItem('url_api');
    this.token_instance = await localforage.getItem('token_instance');

    this.axios = axios.create({
      headers: {
        Authorization: `Token ${this.token_instance}`,
        'Content-Type': 'application/json',
      },
    });
  }

  async syncData() {
    const response = await this.axios.request({
      url: `${this.url_api}/projects/${this.slug_project}/hits/${this.id_hit}?&expand=__batch__settings_batch__template_worker__`,
    });

    this.hit = response.data;
  }
}
