import _ from 'lodash';
import Vue from 'vue';
import SettingsBatch from '../../classes/settings_batch';
import { classesHeaders, initPagination, setPagination } from '../../helpers';
import baseModule from './base.module';

export const moduleSettingsBatch = _.merge({}, baseModule, {
  namespaced: true,
  state: {
    urlApiProjectsSettingsBatch: undefined,
    urlApiProjectsSettingsBatchAll: undefined,

    arrayItems: null,

    paginationGeneral: {
      rowsPerPage: 5,
      sortBy: 'name',
      descending: true,
    },

    arrayColumns: [
      {
        text: 'ID',
        value: 'id',
      },
      {
        text: 'Name',
        value: 'name',
      },
      {
        text: 'Title',
        value: 'title',
        width: '1px',
        align: 'end',
        class: classesHeaders,
      },
      {
        text: 'Reward',
        value: 'reward',
        width: '1px',
        align: 'end',
        class: classesHeaders,
      },
      {
        text: 'Block Workers',
        value: 'block_workers',
        width: '1px',
        align: 'end',
        class: classesHeaders,
      },
      {
        text: '',
        value: 'actions',
        sortable: false,
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
    ],
    objectColumnsSelectedInitialGeneral: {
      name: true,
      title: true,
      reward: true,
      block_workers: true,
      actions: true,
    },
  },
  getters: {
  },
  mutations: {
    setItems(state, { data }) {
      state.arrayItems = [];

      _.forEach(data, (dataSettingsBatch) => {
        const hit = new SettingsBatch(dataSettingsBatch);
        Vue.set(state.arrayItems, state.arrayItems.length, hit);
      });
    },
    update(state, { data }) {
      const settingsBatchNew = new SettingsBatch(data);

      Vue.set(
        state.arrayItems,
        _.findIndex(state.arrayItems, (settingsBatch) => settingsBatch.id === settingsBatchNew.id),
        settingsBatchNew,
      );
    },
    add(state, { data }) {
      const settingsBatchNew = new SettingsBatch(data);

      Vue.set(
        state.arrayItems,
        state.arrayItems.length,
        settingsBatchNew,
      );
    },
    delete(state, { settingsBatch }) {
      Vue.delete(
        state.arrayItems,
        _.findIndex(state.arrayItems, (item) => settingsBatch.id === item.id),
      );
    },
    setUrls(state, config) {
      state.urlApiProjectsSettingsBatch = config.url_api_projects_settings_batch;
      state.urlApiProjectsSettingsBatchAll = config.url_api_projects_settings_batch_all;
    },
  },
  actions: {
    async init({ dispatch }) {
      await Promise.all([
        /**
         * init pagination
         */
        dispatch('loadState', {
          nameLocalStorage: 'pagination_settings_batch_general',
          nameState: 'paginationGeneral',
        }),
      ]);
    },
  },
});
