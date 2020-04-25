import { ServiceEndpoint } from './endpoint.service';
import { store } from '../store/vuex';
import { SettingsBatch } from '../classes/settings_batch';
import { BaseLoadPageService } from './baseLoadPage.service';

class ClassSettingsBatch extends BaseLoadPageService {
  async loadPage(pagination, filters) {
    const project = store.getters['moduleProjects/get_project_current'];

    return ClassSettingsBatch.loadPageInternal({
      pagination,
      filters,
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
        ),
        project,
      },
      callback(response) {
        store.commit('moduleSettingsBatch/setState', {
          objectState: response.data.data.map((settingsBatch) => new SettingsBatch(settingsBatch)),
          nameState: 'arrayItems',
        });
      },
    });
  }

  async getAll() {
    const project = store.getters['moduleProjects/get_project_current'];

    const response = await ServiceEndpoint.makeRequest({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatchAll',
          'moduleSettingsBatch',
        ),
        project,
      },
      params: {
        fields: [
          'id',
          'name',
        ],
      },
    });

    return response.data;
  }

  async get(idSettingsBatch) {
    const project = store.getters['moduleProjects/get_project_current'];

    const response = await ServiceEndpoint.makeRequest({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
        ),
        value: idSettingsBatch,
        project,
      },
    });

    return new SettingsBatch(response.data);
  }

  async create({ settingsBatch, project }) {
    const response = await ServiceEndpoint.makeRequest({
      method: 'post',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
        ),
        project,
      },
      data: settingsBatch,
    });

    store.commit('moduleSettingsBatch/add', {
      data: response.data,
    });
  }

  async edit({ settingsBatchCurrent, settingsBatchNew, project }) {
    const dataChanged = settingsBatchCurrent.getChanges(settingsBatchNew);

    if (Object.keys(dataChanged).length === 0) return;

    const response = await ServiceEndpoint.makeRequest({
      method: 'put',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
        ),
        value: settingsBatchCurrent.id,
        project,
      },
      data: dataChanged,
    });

    store.commit('moduleSettingsBatch/update', {
      data: response.data,
    });
  }

  async delete({ settingsBatch, project, callback }) {
    await ServiceEndpoint.makeRequest({
      method: 'delete',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
        ),
        project,
        value: settingsBatch.id,
      },
    });

    callback();
    store.commit('moduleSettingsBatch/delete', {
      settingsBatch,
    });
  }
}

export const ServiceSettingsBatch = new ClassSettingsBatch();
