import { store } from '../store/vuex';
import { Service_Endpoint } from './service_endpoint';
import { Service_Projects } from './service_projects';
import queue from '../queue';

class Class_Service_App {
  async init(force = false) {
    const isSuccess = await store.dispatch('module_app/load_credentials');

    if (isSuccess === false) {
      return {
        reason: 'load_credentials',
      };
    }

    Service_Endpoint.init(force);

    const response = await this.loadConfig();

    if(response.success) {
      await Service_Projects.load_projects();
      await Service_Projects.load_project_data();
    }

    return response;
  }

  async loadConfig() {
    const response = await Service_Endpoint.make_request({
      url: {
        path: 'config',
      },
      method: 'get',
    });

    if(response.success === true) {
      await store.dispatch('module_app/init', response.data);
    }

    return response;
  }

  async updateCredentials({ url, token, router }) {
    url = url.trim();

    if (!url.startsWith('http')) {
      url = `http://${url}`;
    }

    if (url.endsWith('/')) {
      url = url.slice(0, -1);
    }

    await store.dispatch('module_app/setState', {
      objectState: url,
      nameState: 'url_api',
      nameLocalStorage: 'url_api',
    });

    await store.dispatch('module_app/setState', {
      objectState: token,
      nameState: 'token_instance',
      nameLocalStorage: 'token_instance',
    });

    const response = await this.init(true);

    if(response.success === true) {
      // send the user to the dashboard if no error occured
      queue.notify('router', { name: 'dashboard' });
    }
  }
}

export const Service_App = new Class_Service_App();
