import _ from 'lodash';
import Vue from 'vue';
import Settings_Batch from '../../classes/settings_batch';

export const moduleSettingsBatch = {
  namespaced: true,
  state: {
    arrayItems: null,

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
        text: 'Actions',
        value: 'actions',
        sortable: false,
      },
    ],
  },
  getters: {
    arrayItems: state => () => state.arrayItems,
  },
  mutations: {
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
  },
};
