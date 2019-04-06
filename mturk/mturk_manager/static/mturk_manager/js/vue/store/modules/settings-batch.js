import _ from 'lodash';
import Vue from 'vue';
import Settings_Batch from '../../classes/settings_batch';
import {initPagination, setPagination} from '../../helpers';
import localforage from "localforage";
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
        classes: ['text-xs-left', 'pl-3'],
      },
      {
        text: 'Title',
        value: 'title',
        classes: ['text-xs-left'],
      },
      {
        text: 'Reward',
        value: 'reward',
        classes: ['text-xs-right'],
      },
      {
        text: 'Block Workers',
        value: 'block_workers',
      },
      {
        text: 'Actions',
        value: 'actions',
        sortable: false,
        width: '10%',
      },
    ],
  },
  getters: {
  },
  mutations: {
    setPaginationGeneral(state, { pagination, setPageTo1 }) {
      setPagination({
        pagination,
        setPageTo1,
        namePagination: 'paginationGeneral',
        nameLocalStorage: 'pagination_settings_batch_general',
        state,
      });
    },
    setItems(state, { data }) {
      state.arrayItems = [];

      _.forEach(data, (dataSettingsBatch) => {
        const hit = new Settings_Batch(dataSettingsBatch);
        Vue.set(state.arrayItems, state.arrayItems.length, hit);
      });
    },
    update(state, { data }) {
      const settingsBatchNew = new Settings_Batch(data);

      Vue.set(
        state.arrayItems,
        _.findIndex(state.arrayItems, settingsBatch => settingsBatch.id === settingsBatchNew.id),
        settingsBatchNew,
      );
    },
    add(state, { data }) {
      const settingsBatchNew = new Settings_Batch(data);

      Vue.set(
        state.arrayItems,
        state.arrayItems.length,
        settingsBatchNew,
      );
    },
    delete(state, { settingsBatch }) {
      Vue.delete(
        state.arrayItems,
        _.findIndex(state.arrayItems, item => settingsBatch.id === item.id),
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
