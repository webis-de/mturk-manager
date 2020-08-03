import { ServiceEndpoint } from './endpoint.service';

export class BaseLoadPageService {
  static async loadPageInternal({
    pagination, filters, method = 'get', url, callback,
  }) {
    const response = await ServiceEndpoint.makeRequest({
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
