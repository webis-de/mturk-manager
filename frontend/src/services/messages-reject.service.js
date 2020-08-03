import { ServiceEndpoint } from './endpoint.service';
import { store } from '../store/vuex';
import { BaseLoadPageService } from './baseLoadPage.service';

class ClassServiceMessagesReject extends BaseLoadPageService {
  async loadPageReject(pagination, filters) {
    return ClassServiceMessagesReject.loadPageInternal({
      pagination,
      filters,
      url: {
        path: store.getters.get_url(
          'urlApiProjectsMessagesReject',
          'moduleMessages',
        ),
        project: store.getters['moduleProjects/get_project_current'],
      },
      callback(response) {
        store.commit('moduleMessages/setState', {
          objectState: response.data.data,
          nameState: 'arrayItemsReject',
        });
      },
    });
  }

  async loadPageRejectAll(pagination, filters) {
    return ClassServiceMessagesReject.loadPageInternal({
      pagination,
      filters,
      url: {
        path: store.getters.get_url(
          'urlApiMessagesReject',
          'moduleMessages',
        ),
      },
      callback(response) {
        store.commit('moduleMessages/setState', {
          objectState: response.data.data,
          nameState: 'arrayItemsReject',
        });
      },
    });
  }

  async loadAll({ search }) {
    const response = await ServiceEndpoint.makeRequest({
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
    const response = await ServiceEndpoint.makeRequest({
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
    const response = await ServiceEndpoint.makeRequest({
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
    const response = await ServiceEndpoint.makeRequest({
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

export const ServiceMessages = new ClassServiceMessagesReject();
