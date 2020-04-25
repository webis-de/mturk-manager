import Vue from 'vue';
import _ from 'lodash';
import localforage from 'localforage';
import HIT from '../../classes/hit.js';

import Batch from '../../classes/batch';
import {classesHeaders, initPagination, setPagination} from '../../helpers';
import baseModule from './base.module';

export const moduleHITs = _.merge({}, baseModule, {
  namespaced: true,
  state: {
    object_hits: {},
    object_hits_sandbox: {},

    arrayHITs: null,
    arrayHITsSandbox: null,

    url_api_projects_hits: undefined,
    url_api_hits: undefined,

    object_hits_selected: {},

    paginationGeneral: {
      itemsPerPage: 25,
      sortBy: ['datetime_creation'],
      sortDesc: [true],
    },

    paginationFinances: {
      itemsPerPage: 5,
      sortBy: ['datetime_creation'],
      sortDesc: [true],
    },

    array_columns_general: [
      {
        text: 'ID',
        value: 'id_hit',
        class: classesHeaders,
      },
      {
        text: 'Batch',
        value: 'batch',
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
      {
        text: 'Creation',
        value: 'datetime_creation',
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
      {
        text: 'Progress',
        value: 'progress',
        align: 'end',
        sortable: false,
        class: classesHeaders,
        width: '1px',
      },
      // {
      //   text: '',
      //   value: 'actions',
      //   sortable: false,
      //   label: 'Details',
      // },
    ],
    objectColumnsSelectedInitialGeneral: {
      id_hit: true,
      batch: true,
      datetime_creation: true,
      progress: true,
      actions: true,
    },
    objectColumnsSelectedInitialFinances: {
      id_hit: true,
      batch: true,
      datetime_creation: true,
      progress: true,
      actions: true,
    },
    objectColumnsSelectedGeneral: null,
    objectColumnsSelectedFinances: null,

    objectFiltersGeneral: null,
    objectFiltersFinances: null,
    objectFiltersDefaultGeneral: {
      hitsSelected: [],
      batchesSelected: [],
    },
  },
  getters: {
    get_array_columns_general: state => state.array_columns_general,
    get_array_columns_selected_general: (state) => {
      if (state.array_columns_selected_general === null) {
        return state.array_columns_selected_initial_general;
      }
      return state.array_columns_selected_general;
    },
    get_array_columns_selected_initial_general: state => state.array_columns_selected_initial_general,

    get_object_hits_selected: state => state.object_hits_selected,
    get_array_hits: (state, getters, rootState) => (
      use_sandbox = undefined,
    ) => {
      if (use_sandbox === undefined) {
        return rootState.module_app.use_sandbox
          ? state.array_hits_sandbox
          : state.array_hits;
      }
      return use_sandbox ? state.array_hits_sandbox : state.array_hits;
    },
    get_array_hits_sandbox: state => state.array_hits_sandbox,
    get_object_hits: (state, getters, rootState) => (
      use_sandbox = undefined,
    ) => {
      if (use_sandbox == undefined) {
        return rootState.module_app.use_sandbox
          ? state.object_hits_sandbox
          : state.object_hits;
      }
      return use_sandbox ? state.object_hits_sandbox : state.object_hits;
    },
    list_hits: (state, getters) => {
      if (Object.keys(getters.get_object_hits()).length == 0) {
        return [];
      }
      return _.orderBy(
        getters.get_object_hits(),
        ['datetime_creation'],
        ['desc'],
      );
    },
  },
  mutations: {
    setItemsSelected(state, { items }) {
      state.object_hits_selected = items;
    },
    setPaginationGeneral(state, { pagination, setPageTo1 }) {
      setPagination({
        pagination,
        setPageTo1,
        namePagination: 'paginationGeneral',
        nameLocalStorage: 'pagination_hits_general',
        state,
      });
    },
    setPaginationFinances(state, { pagination, setPageTo1 }) {
      setPagination({
        pagination,
        setPageTo1,
        namePagination: 'paginationFinances',
        nameLocalStorage: 'pagination_hits_finances',
        state,
      });
    },
    set_array_columns_general(state, array_columns) {
      localforage.setItem('array_columns_hits_general', array_columns);
      state.array_columns_selected_general = array_columns;
    },

    set_hits(state, { data, use_sandbox }) {
      let array_hits = null;
      if (use_sandbox) {
        state.array_hits_sandbox = [];
        array_hits = state.array_hits_sandbox;
      } else {
        state.array_hits = [];
        array_hits = state.array_hits;
      }

      _.forEach(data, (data) => {
        const hit = new HIT(data);
        Vue.set(array_hits, array_hits.length, hit);
      });
    },
    clear_hits_selected(state) {
      state.object_hits_selected = {};
    },
    set_hits_selected(state, { array_items, add }) {
      if (add === true) {
        _.forEach(array_items, (item) => {
          Vue.set(state.object_hits_selected, item.id, item.id);
        });
      } else {
        _.forEach(array_items, (item) => {
          Vue.delete(state.object_hits_selected, item.id);
        });
      }
    },
    // set_hits(state, {object_batches, data_batches, use_sandbox}) {
    //     let object_hits = null;
    //     if(use_sandbox)
    //     {
    //         object_hits = state.object_hits_sandbox;
    //     } else {
    //         object_hits = state.object_hits;
    //     }
    //
    //     _.forEach(data_batches, function(data_batch) {
    //     	const id_batch = data_batch.id;
    //     	const batch = object_batches[id_batch];
    //
    //         _.forEach(data_batch.hits, function(data_hit) {
    //         	data_hit.batch = batch;
    //             const hit = new HIT(data_hit);
    //
    //             Vue.set(object_hits, hit.id, hit);
    //
    //             Vue.set(batch.object_hits, hit.id, hit);
    //         });
    //     });
    // },
    clear_sandbox(state) {
      state.object_hits_sandbox = {};
    },
    reset: (state) => {
      state.object_hits = {};
      state.object_hits_sandbox = {};
    },
    set_urls(state, config) {
      state.url_api_projects_hits = config.url_api_projects_hits;
      state.url_api_hits = config.url_api_hits;
    },
  },
  actions: {
    async init({ state, commit, dispatch }) {
      await Promise.all([
        /**
         * init columns
         */
        dispatch('loadState', {
          nameLocalStorage: 'array_columns_hits_general',
          nameState: 'objectColumnsSelectedGeneral',
          objectStateDefault: state.objectColumnsSelectedInitialGeneral,
        }),
        dispatch('loadState', {
          nameLocalStorage: 'array_columns_hits_finances',
          nameState: 'objectColumnsSelectedFinances',
          objectStateDefault: state.objectColumnsSelectedInitialFinances,
        }),
        /**
         * init paginations
         */
        dispatch('loadState', {
          nameLocalStorage: 'pagination_hits_general',
          nameState: 'paginationGeneral',
        }),
        dispatch('loadState', {
          nameLocalStorage: 'pagination_hits_finances',
          nameState: 'paginationFinances',
        }),
        /**
         * init filters
         */
        dispatch('loadState', {
          nameLocalStorage: 'filtersHITsGeneral',
          nameState: 'objectFiltersGeneral',
          objectStateDefault: state.objectFiltersDefaultGeneral,
        }),
        dispatch('loadState', {
          nameLocalStorage: 'filtersHITsFinances',
          nameState: 'objectFiltersFinances',
          objectStateDefault: state.objectFiltersDefaultGeneral,
        }),
      ]);
    },
    setItemsSelected({ commit }, data) {
      commit(
        'setItemsSelected',
        data,
      );
    },
    reset_array_columns_general({ state, commit }) {
      commit(
        'set_array_columns_general',
        state.objectColumnsSelectedInitialGeneral,
      );
    },
  },
});
