import { Service_Endpoint } from './service_endpoint';
import { store } from '../store/vuex';

class Class_Service_Messages_Reject {
  async loadPageReject(pagination, filters) {
    const response = await Service_Endpoint.make_request({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsMessagesReject',
          'moduleMessages',
        ),
        project: store.getters['moduleProjects/get_project_current'],
      },
      params: {
        page: pagination.page,
        page_size: pagination.rowsPerPage,
        sort_by: pagination.sortBy,
        descending: pagination.descending,
        ...filters,
      },
    });

    store.commit('moduleMessages/setState', {
      objectState: response.data.data,
      nameState: 'arrayItemsReject',
    });

    return response.data.items_total;
  }

  async loadPageRejectAll(pagination, filters) {
    const response = await Service_Endpoint.make_request({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'urlApiMessagesReject',
          'moduleMessages',
        ),
      },
      params: {
        page: pagination.page,
        page_size: pagination.rowsPerPage,
        sort_by: pagination.sortBy,
        descending: pagination.descending,
        ...filters,
      },
    });

    store.commit('moduleMessages/setState', {
      objectState: response.data.data,
      nameState: 'arrayItemsReject',
    });

    return response.data.items_total;
  }

  async loadAll({ search }) {
    const response = await Service_Endpoint.make_request({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'urlApiMessagesReject',
          'moduleMessages',
        ),
      },
      params: {
        search,
        limit: 10,
        sort_by: 'count_usage',
        descending: true,
      },
    });

    return response.data.data;
  }

  async save({ message }) {
    const response = await Service_Endpoint.make_request({
      method: 'post',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsMessagesReject',
          'moduleMessages',
        ),
        project: store.getters['moduleProjects/get_project_current'],
      },
      data: message,
    });

    console.warn('response', response);
  }

  async setDefault({ idMessage }) {
    const response = await Service_Endpoint.make_request({
      method: 'put',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsMessagesReject',
          'moduleMessages',
        ),
        project: store.getters['moduleProjects/get_project_current'],
        value: idMessage,
      },
    });

    console.warn('response', response);
  }

  async delete({ idMessage }) {
    const response = await Service_Endpoint.make_request({
      method: 'delete',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsMessagesReject',
          'moduleMessages',
        ),
        project: store.getters['moduleProjects/get_project_current'],
        value: idMessage,
      },
    });

    console.warn('response', response);
  }
}

export const ServiceMessages = new Class_Service_Messages_Reject();
