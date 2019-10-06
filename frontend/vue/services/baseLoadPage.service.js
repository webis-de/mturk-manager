import { Service_Endpoint } from './service_endpoint';
import { store } from '../store/vuex';

export class BaseLoadPageService {
  static async loadPage({ pagination, filters, method = 'get', url, callback}) {
    const response = await Service_Endpoint.make_request({
      method,
      url,
      params: {
        page: pagination.page,
        page_size: pagination.itemsPerPage,
        sort_by: pagination.sortBy[0],
        descending: pagination.sortDesc[0],
        ...filters,
      },
    });

    if (callback !== undefined) {
      callback(response);
    }

    return response.data.items_total;
  }
}
