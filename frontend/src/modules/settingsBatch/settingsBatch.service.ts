import { store } from '@/store/vuex';
import {
  queryCreateSettingsBatch,
  queryDeleteSettingsBatch,
  querySettingsBatch, queryUpdateSettingsBatch,
} from '@/modules/settingsBatch/settingsBatch.graphql';
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';
import { ServiceEndpoint } from '@/services/endpoint.service';

class ClassServiceSettingsBatch {
  async loadSettingsBatch() {
    const response = await ServiceEndpoint.apolloClient.query({
      query: querySettingsBatch,
      variables: {
        project: store.getters['moduleProjects/get_project_current'].id,
      },
      fetchPolicy: 'no-cache',
    });

    store.commit('moduleSettingsBatch/setSettingsBatch', {
      settingsBatches: await SettingsBatch.convertFromServerToStore<SettingsBatch>(response.data.settingsBatch),
    });
  }

  async create({
    settingsBatch,
  }: { settingsBatch: SettingsBatch }) {
    const response = await ServiceEndpoint.apolloClient.query({
      query: queryCreateSettingsBatch,
      variables: {
        settingsBatch: settingsBatch.prepareForServer(),
      },
      fetchPolicy: 'no-cache',
    });

    store.commit('moduleSettingsBatch/createSettingsBatch', {
      settingsBatch: await SettingsBatch.parseFromServer(response.data.createSettingsBatch.settingsBatch),
    });
  }

  async update({
    settingsBatch,
  }: { settingsBatch: SettingsBatch }) {
    console.log(settingsBatch, 'settingsBatch');
    const response = await ServiceEndpoint.apolloClient.query({
      query: queryUpdateSettingsBatch,
      variables: {
        settingsBatch: settingsBatch.prepareForServer(),
      },
      fetchPolicy: 'no-cache',
    });

    store.commit('moduleSettingsBatch/updateSettingsBatch', {
      settingsBatch: await SettingsBatch.parseFromServer(response.data.updateSettingsBatch.settingsBatch),
    });
  }

  async delete({
    settingsBatch,
  }: { settingsBatch: SettingsBatch }) {
    await ServiceEndpoint.apolloClient.query({
      query: queryDeleteSettingsBatch,
      variables: {
        id: settingsBatch.id,
      },
      fetchPolicy: 'no-cache',
    });

    store.commit('moduleSettingsBatch/deleteSettingsBatch', {
      settingsBatch,
    });
  }
}

export const ServiceSettingsBatch = new ClassServiceSettingsBatch();
