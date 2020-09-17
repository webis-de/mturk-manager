import Vue from 'vue';
import _ from 'lodash';
import localforage from 'localforage';
import Batch from '../../classes/batch';
import { classesHeaders, setPagination } from '../../helpers';
import baseModule from './base.module';

export const moduleBatches = _.merge({}, baseModule, {
  state: {
    object_batches: null,
    object_batches_sandbox: null,

    arrayBatches: null,
    arrayBatchesSandbox: null,

    url_api_assignments_real_approved: undefined,

    url_api_batches: undefined,
    url_api_projects_batches: undefined,
    url_api_projects_batches_download: undefined,
    url_api_projects_batches_download_info: undefined,
    urlApiProjectsBatchesImport: undefined,

    object_batches_selected: {},

    /**
     * batch creation
     */
    objectCSVParsed: null,
    objectSettingsBatch: null,

    is_syncing_mturk: false,

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
        value: 'name',
        text: 'Name',
        class: classesHeaders,
      },
      {
        text: 'Creation',
        value: 'datetime_creation',
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
      {
        text: 'HITs',
        value: 'count_hits',
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
      {
        text: 'Asgmnts/HIT',
        value: 'settings_batch__count_assignments',
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
      {
        text: 'Assignments',
        value: 'count_assignments_total',
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
      {
        text: 'Workers',
        value: 'count_workers',
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
      {
        text: 'Approved',
        value: 'count_assignments_approved',
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
      {
        text: 'Rejected',
        value: 'count_assignments_rejected',
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
      {
        text: 'Reward ($)',
        value: 'settings_batch__reward',
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
      {
        text: 'Max costs ($)',
        value: 'costs_max',
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
      {
        text: 'Costs So Far ($)',
        value: 'costs_so_far',
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
      name: true,
      count_hits: true,
      datetime_creation: true,
      settings_batch__count_assignments: true,
      count_assignments_total: true,
      count_workers: true,
      progress: true,
      actions: true,
    },
    objectColumnsSelectedGeneral: null,
    objectColumnsSelectedInitialFinances: {
      name: true,
      count_hits: true,
      settings_batch__count_assignments: true,
      settings_batch__reward: true,
      count_assignments_total: true,
      count_assignments_approved: true,
      count_assignments_rejected: true,
      costs_max: true,
      costs_so_far: true,
    },
    objectColumnsSelectedFinances: null,

    objectFiltersGeneral: null,
    objectFiltersFinances: null,

    objectFiltersDefaultGeneral: {
      batchesSelected: [],
      workersSelected: [],
    },
  },
  getters: {
    get_array_columns_general: state => state.array_columns_general,
    get_array_columns_selected_initial_general: state => state.array_columns_selected_initial_general,

    get_array_columns_selected_finances: (state) => {
      if (state.array_columns_selected_finances === null) {
        return state.array_columns_selected_initial_finances;
      }
      return state.array_columns_selected_finances;
    },
    get_array_columns_selected_initial_finances: state => state.array_columns_selected_initial_finances,
    list_hits_for_csv: (state) => {
      const list_hits = [];
      _.forIn(state.object_batches, (batch, id_batch) => {
        _.forEach(batch.hits, (hit) => {
          list_hits.push([
            hit.id_hit,
            (hit.count_assignments * batch.reward).toFixed(2),
            id_batch,
          ]);
        });
      });
      return list_hits;
    },
    get_is_syncing_mturk: state => state.is_syncing_mturk,
  },
  mutations: {
    setItemsSelected(state, { items }) {
      state.object_batches_selected = items;
    },
    set_array_columns_general(state, array_columns) {
      localforage.setItem('array_columns_batches_general', array_columns);
      state.array_columns_selected_general = array_columns;
    },
    set_array_columns_finances(state, array_columns) {
      localforage.setItem('array_columns_batches_finances', array_columns);
      state.array_columns_selected_finances = array_columns;
    },
    clear_batches_selected(state) {
      state.object_batches_selected = {};
    },
    set_batches_selected(state, { array_items, add }) {
      if (add === true) {
        _.forEach(array_items, (item) => {
          Vue.set(state.object_batches_selected, item.id, item.id);
        });
      } else {
        _.forEach(array_items, (item) => {
          Vue.delete(state.object_batches_selected, item.id);
        });
      }
    },
    // append_batches(state, {data_batches, use_sandbox}) {
    //     let object_batches = null;
    //     if(use_sandbox)
    //     {
    //         object_batches = state.object_batches_sandbox;
    //     } else {
    //         object_batches = state.object_batches;
    //     }

    //     _.forEach(data_batches, function(data_batch){
    //         const batch = new Batch(data_batch);
    //         Vue.set(object_batches, batch.id, batch);
    //     });
    // },
    add_workers(state, { object_workers, use_sandbox }) {
      // console.log('#####')
      let object_batches = null;
      if (use_sandbox) {
        object_batches = state.object_batches_sandbox;
      } else {
        object_batches = state.object_batches;
      }
      _.forEach(object_batches, (batch) => {
        _.forEach(batch.object_hits, (hit) => {
          _.forEach(hit.object_assignments, (assignment) => {
            if (_.isObject(assignment.worker)) {
              // skip if assignment has already worker
              return true;
            }
            Vue.set(assignment, 'worker', object_workers[assignment.worker]);
            // assignment.worker = object_workers[assignment.worker];
            // Vue.set(assignment.worker, );
          });
        });
      });
    },
    add_batch(state, { data_batch, use_sandbox }) {
      let object_batches = null;
      if (use_sandbox) {
        object_batches = state.object_batches_sandbox;
      } else {
        object_batches = state.object_batches;
      }

      const obj_batch = new Batch(data_batch);
      Vue.set(object_batches, obj_batch.id, obj_batch);

      // _.forEach(data_batch.hits, function(data_hit) {
      //     data_hit.batch = batch;
      //     const hit = new HIT(data_hit);

      //     Vue.set(object_hits, hit.id, hit);

      //     Vue.set(batch.hits, batch.hits.length, hit);
      // });
    },
    set_urls(state, config) {
      state.url_api_batches = config.url_api_batches;
      state.url_api_projects_batches = config.url_api_projects_batches;
      state.url_api_projects_batches_download = config.url_api_projects_batches_download;
      state.url_api_projects_batches_download_info = config.url_api_projects_batches_download_info;
      state.urlApiProjectsBatchesImport = config.url_api_projects_batches_import;
    },
    set_is_syncing_mturk(state, value) {
      state.is_syncing_mturk = value;
    },
    clear_sandbox(state) {
      state.object_batches_sandbox = {};
    },
    reset: (state) => {
      state.object_batches = null;
      state.object_batches_sandbox = null;
      state.objectCSVParsed = null;
      state.is_syncing_mturk = false;
    },
  },
  actions: {
    async init({ state, dispatch }) {
      await Promise.all([
        /**
         * init columns
         */
        dispatch('loadState', {
          nameLocalStorage: 'array_columns_batches_general',
          nameState: 'objectColumnsSelectedGeneral',
          objectStateDefault: state.objectColumnsSelectedInitialGeneral,
        }),
        dispatch('loadState', {
          nameLocalStorage: 'array_columns_batches_finances',
          nameState: 'objectColumnsSelectedFinances',
          objectStateDefault: state.objectColumnsSelectedInitialFinances,
        }),
        /**
         * init pagination
         */
        dispatch('loadState', {
          nameLocalStorage: 'pagination_batches_general',
          nameState: 'paginationGeneral',
        }),
        dispatch('loadState', {
          nameLocalStorage: 'pagination_batches_finances',
          nameState: 'paginationFinances',
        }),
        /**
         * init filters
         */
        dispatch('loadState', {
          nameLocalStorage: 'filtersBatchesGeneral',
          nameState: 'objectFiltersGeneral',
          objectStateDefault: state.objectFiltersDefaultGeneral,
        }),
        dispatch('loadState', {
          nameLocalStorage: 'filtersBatchesFinances',
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
    reset_array_columns_finances({ state, commit }) {
      commit(
        'set_array_columns_finances',
        state.objectColumnsSelectedInitialFinances,
      );
    },
  },
});
