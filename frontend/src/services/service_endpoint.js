import axios from 'axios';
import { store } from '../store/vuex';
import queue from '../queue';

class Class_Service_Endpoint {
  constructor() {
    this.is_initialized = false;
    this.axios = undefined;
  }

  init(force = false) {
    if (this.is_initialized === true && force === false) {
      console.error('Service Endpoint is already initialized!');
      return;
    }

    this.is_initialized = true;

    this.axios = axios.create({
      headers: {
        Authorization: `Token ${store.state.module_app.token_instance}`,
        'Content-Type': 'application/json',
      },
    });
  }

  async make_request({
    url, method, data, params, options,
  }) {
    const config = {
      method,
      url: this.get_url_api(url),
      data: JSON.stringify(data),
      params,
      ...options,
    };

    const object_response = {
      success: undefined,
      response: undefined,
      exception: undefined,
      data: undefined,
    };

    try {
      object_response.response = await this.axios.request(config);

      object_response.success = true;
      object_response.data = object_response.response.data;
    } catch (exception) {
      object_response.exception = exception;
      object_response.success = false;
    }

    if (object_response.success === false) {
      // only send to connection_error if its an request to the api
      if (object_response.exception.message === 'Network Error' && url.host === undefined) {
        queue.notify('router', { name: 'connection_error' });
      } else {
        console.warn('Error', object_response.exception);
        // queue.notify('router', { name: 'connection_error' });
      }
    }

    return object_response;
  }

  get_url_api({
    host,
    path = '',
    use_sandbox,
    value,
    project,
  }) {
    // TODO: Fix this approach
    // let url = new URL(path, store.state.module_app.url_api);

    let url;
    if(host !== undefined) {
      url = `${host}/${path}`;
    } else {
      url = `${store.state.module_app.url_api}/${path}`;
    }

    if (value !== undefined) {
      url += `/${value}`;
    }

    const params = new URLSearchParams();

    if (use_sandbox === false) {
      params.append('use_sandbox', 'false');
    }

    url += `?${params.toString()}`;

    if (project) {
      url = url.replace('PLACEHOLDER_SLUG_PROJECT', project.slug);
    }
    // url = url.replace('PLACEHOLDER_SLUG_PROJECT',  getters['moduleProjects/get_project_current'].slug);
    return url;
  }
}

export const Service_Endpoint = new Class_Service_Endpoint();
// export default new Service_Endpoint();
