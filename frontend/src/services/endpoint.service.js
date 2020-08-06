import axios from 'axios';
import { createApolloClient } from 'vue-cli-plugin-apollo/graphql-client';
import { defaultOptionsApollo } from '@/vue-apollo';
import { store } from '../store/vuex';
import queue from '../queue';

class ClassServiceEndpoint {
  constructor() {
    this.is_initialized = false;
    this.axios = undefined;

    this.apolloClient = null;
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

    this.refreshApolloClient();
  }

  async makeRequest({
    url, method, data, params, options,
  }) {
    const config = {
      method,
      url: this.getUrlApi(url),
      data: JSON.stringify(data),
      params,
      ...options,
    };

    const objectResponse = {
      success: undefined,
      response: undefined,
      exception: undefined,
      data: undefined,
    };

    try {
      objectResponse.response = await this.axios.request(config);

      objectResponse.success = true;
      objectResponse.data = objectResponse.response.data;
    } catch (exception) {
      objectResponse.exception = exception;
      objectResponse.success = false;
    }

    if (objectResponse.success === false) {
      // only send to connection_error if its an request to the api
      if (objectResponse.exception.message === 'Network Error' && url.host === undefined) {
        queue.notify('router', { name: 'connection_error' });
      } else {
        console.warn('Error', objectResponse.exception);
        // queue.notify('router', { name: 'connection_error' });
      }
    }

    return objectResponse;
  }

  getUrlApi({
    host,
    path = '',
    use_sandbox,
    value,
    project,
  }) {
    // TODO: Fix this approach
    // let url = new URL(path, store.state.module_app.url_api);

    let url;
    if (host !== undefined) {
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

  refreshApolloClient() {
    const { apolloClient } = createApolloClient({
      ...defaultOptionsApollo,
      ...{ httpEndpoint: `${store.state.module_app.url_api}/graphql` },
    });

    this.apolloClient = apolloClient;
  }
}

export const ServiceEndpoint = new ClassServiceEndpoint();
// export default new ServiceEndpoint();
