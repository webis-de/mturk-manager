import _ from 'lodash';
import Vue from 'vue';
import baseModule from '@/store/modules/base.module';
import { TemplateAssignment } from '@/modules/template/templateAssignment.model';
import { TemplateHIT } from '@/modules/template/templateHIT.model';
import { TemplateGlobal } from '@/modules/template/templateGlobal.model';
import { TemplateWorker } from '@/modules/template/templateWorker.model';
import { classesHeaders } from '@/helpers';
import { TemplateBase } from '@/modules/template/templateBase.model';
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';

interface StoreSettingsBatchState {
  settingsBatch: { [key: string]: SettingsBatch};
}

export const moduleSettingsBatch = _.merge({}, baseModule, {
  namespaced: true,
  state: {
    settingsBatch: null,

    paginationGeneral: {
      rowsPerPage: 5,
      sortBy: 'name',
      descending: true,
    },

    arrayColumns: [
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
        value: 'blockWorkers',
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
      blockWorkers: true,
      actions: true,
    },
  },
  getters: {
    settingsBatchSortedByName(state: StoreSettingsBatchState): SettingsBatch[] | null {
      if (state.settingsBatch === null) return null;

      return Object.values(state.settingsBatch).sort((a, b) => a.name.localeCompare(b.name));
    },
  },
  mutations: {
    /**
     * Set
     */
    setSettingsBatch(state: StoreSettingsBatchState, { settingsBatches }: {settingsBatches: { [key: string]: SettingsBatch}}) {
      state.settingsBatch = settingsBatches;
    },
    /**
     * Create
     */
    createSettingsBatch(state: StoreSettingsBatchState, { settingsBatch }: {settingsBatch: SettingsBatch }) {
      if (settingsBatch.id !== undefined) Vue.set(state.settingsBatch, settingsBatch.id, settingsBatch);
    },
    /**
     * Update
     */
    updateSettingsBatch(state: StoreSettingsBatchState, { settingsBatch }: {settingsBatch: SettingsBatch }) {
      if (settingsBatch.id !== undefined) Vue.set(state.settingsBatch, settingsBatch.id, settingsBatch);
    },
    /**
     * Delete
     */
    deleteSettingsBatch(state: StoreSettingsBatchState, { settingsBatch }: {settingsBatch: SettingsBatch }) {
      if (settingsBatch.id !== undefined) Vue.delete(state.settingsBatch, settingsBatch.id);
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
