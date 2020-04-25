import { ServiceEndpoint } from './endpoint.service';
import { store } from '../store/vuex';
import SettingsBatch from '../classes/settings_batch';
import { BaseLoadPageService } from './baseLoadPage.service';

class Class_Settings_Batch extends BaseLoadPageService {
  async loadPage(pagination, filters) {
    const project = store.getters['moduleProjects/get_project_current'];

    return Class_Settings_Batch.loadPageInternal({
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

  async create({ settings_batch, project }) {
    const response = await ServiceEndpoint.makeRequest({
      method: 'post',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
        ),
        project,
      },
      data: settings_batch,
    });

    store.commit('moduleSettingsBatch/add', {
      data: response.data,
    });
  }

  async edit({ settings_batch_current, settings_batch_new, project }) {
    const data_changed = settings_batch_current.getChanges(settings_batch_new);

    if (Object.keys(data_changed).length === 0) return;

    const response = await ServiceEndpoint.makeRequest({
      method: 'put',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
        ),
        value: settings_batch_current.id,
        project,
      },
      data: data_changed,
    });

    store.commit('moduleSettingsBatch/update', {
      data: response.data,
    });
  }

  async delete({ settings_batch, project, callback }) {
    const response = await ServiceEndpoint.makeRequest({
      method: 'delete',
      url: {
        path: store.getters.get_url(
          'urlApiProjectsSettingsBatch',
          'moduleSettingsBatch',
        ),
        project,
        value: settings_batch.id,
      },
    });

    callback();
    store.commit('moduleSettingsBatch/delete', {
      settingsBatch: settings_batch,
    });
  }
}

export const ServiceSettingsBatch = new Class_Settings_Batch();
