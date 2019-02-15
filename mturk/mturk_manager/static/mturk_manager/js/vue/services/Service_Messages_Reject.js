import { Service_Endpoint } from './service_endpoint';
import { store } from '../store/vuex';

class Class_Service_Messages_Reject {
  async load() {
    if (
      store.getters['moduleMessagesReject/get_object_messages_reject'] == null
    ) {
      const response = await Service_Endpoint.make_request({
        method: 'get',
        url: {
          path: store.getters.get_url(
            'url_api_messages_reject',
            'moduleMessagesReject',
          ),
        },
      });

      store.commit('moduleMessagesReject/set_messages_reject', response.data);
    }
  }
}

export const Service_Messages_Reject = new Class_Service_Messages_Reject();
