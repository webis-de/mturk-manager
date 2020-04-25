import { ServiceEndpoint } from './endpoint.service';
import { store } from '../store/vuex';

class ClassServiceKeywords {
  async load() {
    if (store.getters['moduleKeywords/get_object_keywords'] == null) {
      const response = await ServiceEndpoint.makeRequest({
        method: 'get',
        url: {
          path: store.getters.get_url('url_api_keywords', 'moduleKeywords'),
        },
      });

      store.commit('moduleKeywords/set_keywords', response.data);
    }
  }
}

export const ServiceKeywords = new ClassServiceKeywords();
