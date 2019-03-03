import axios from 'axios';
import { store } from '../store/vuex';
import { Service_Endpoint } from './service_endpoint';
import { Service_Projects } from './service_projects';

class Class_Service_App {
  async init() {
    console.warn('init app');
    const isSuccess = await store.dispatch('module_app/load_credentials');

    if (isSuccess === false) {
      return false;
    }
    Service_Endpoint.init(store.state.module_app.token_instance);

    await this.load_config();
    await Service_Projects.load_projects();
    await Service_Projects.load_project_data();
  }

  async load_config() {
    const response = await Service_Endpoint.make_request({
      url: {
        path: 'config',
      },
      method: 'get',
    });

    console.log('config', response.data);

    await store.dispatch('module_app/init', response.data);

    return response.data;
  }

  async load_balance() {
    const use_sandbox = store.state.module_app.use_sandbox;

    const response = await Service_Endpoint.make_request({
      url: {
        path: store.getters.get_url(
          'url_api_projects_balance',
          'module_finances',
        ),
        use_sandbox,
        project: store.getters['moduleProjects/get_project_current'],
      },
      method: 'get',
    });

    if (use_sandbox === true) {
      store.commit(
        'module_finances/set_balance_sandbox',
        response.data.balance,
      );
    } else {
      store.commit('module_finances/set_balance', response.data.balance);
    }
  }
}

export const Service_App = new Class_Service_App();
