import {
  queryCreateTemplateAssignment, queryCreateTemplateGlobal, queryCreateTemplateHIT, queryCreateTemplateWorker,
  queryDeleteTemplateAssignment,
  queryDeleteTemplateGlobal, queryDeleteTemplateHIT, queryDeleteTemplateWorker,
  queryTemplates,
  queryUpdateTemplateAssignment, queryUpdateTemplateGlobal, queryUpdateTemplateHIT,
  queryUpdateTemplateWorker,
} from '@/modules/template/template.graphql';
import { apolloClient } from '@/vue-apollo';
import { store } from '@/store/vuex';
import { TemplateWorker } from '@/modules/template/templateWorker.model';
import { TemplateAssignment } from '@/modules/template/templateAssignment.model';
import { TemplateHIT } from '@/modules/template/templateHIT.model';
import { TemplateGlobal } from '@/modules/template/templateGlobal.model';
import { TemplateBase } from '@/modules/template/templateBase.model';
import {
  queryCreateSettingsBatch,
  queryDeleteSettingsBatch,
  querySettingsBatch, queryUpdateSettingsBatch,
} from '@/modules/settingsBatch/settingsBatch.graphql';
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';

class ClassServiceSettingsBatch {
  async loadSettingsBatch() {
    const response = await apolloClient.query({
      query: querySettingsBatch,
      variables: {
        project: store.getters['moduleProjects/get_project_current'].id,
      },
      fetchPolicy: 'no-cache',
    });

    store.commit('moduleSettingsBatch/setSettingsBatch', {
      settingsBatches: SettingsBatch.prepareFromServerToStore(response.data.settingsBatch),
    });
  }

  async create({
    settingsBatch,
  }: { settingsBatch: SettingsBatch }) {
    const response = await apolloClient.query({
      query: queryCreateSettingsBatch,
      variables: {
        settingsBatch: settingsBatch.extractBody(),
      },
      fetchPolicy: 'no-cache',
    });

    store.commit('moduleSettingsBatch/createSettingsBatch', {
      settingsBatch: SettingsBatch.parseFromServer(response.data.createSettingsBatch.settingsBatch),
    });
  }

  async update({
    settingsBatch,
  }: { settingsBatch: SettingsBatch }) {
    console.log(settingsBatch, 'settingsBatch');
    const response = await apolloClient.query({
      query: queryUpdateSettingsBatch,
      variables: {
        settingsBatch: settingsBatch.extractBody(),
      },
      fetchPolicy: 'no-cache',
    });

    store.commit('moduleSettingsBatch/updateSettingsBatch', {
      settingsBatch: SettingsBatch.parseFromServer(response.data.updateSettingsBatch.settingsBatch),
    });
  }

  async delete({
    settingsBatch,
  }: { settingsBatch: SettingsBatch }) {
    await apolloClient.query({
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
