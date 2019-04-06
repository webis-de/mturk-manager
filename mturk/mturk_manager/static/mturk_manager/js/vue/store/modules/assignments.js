import Vue from 'vue';
import _ from 'lodash';
import localforage from 'localforage';
import Assignment from '../../classes/assignment.js';

import HIT from '../../classes/hit';
import { initPagination, setPagination } from '../../helpers';
import baseModule from './base.module';

export const moduleAssignments = _.merge({}, baseModule, {
  state: {
    object_assignments: {},
    object_assignments_sandbox: {},

    array_assignments: null,
    array_assignments_sandbox: null,
    url_api_projects_assignments: undefined,

    set_ids_worker: null,
    object_assignments_selected: {},

    paginationGeneral: {
      rowsPerPage: 25,
      sortBy: 'datetime_creation',
      descending: true,
    },

    paginationFinances: {
      rowsPerPage: 5,
      sortBy: 'datetime_creation',
      descending: true,
    },

    array_columns_general: [
      {
        text: 'ID',
        value: 'id_assignment',
        classes: ['text-xs-left'],
      },
      {
        text: 'Creation',
        value: 'datetime_creation',
      },
      {
        text: 'Accepted',
        value: 'datetime_accept',
      },
      {
        text: 'Submitted',
        value: 'datetime_submit',
      },
      {
        text: 'Duration',
        value: 'duration',
      },
      {
        text: 'Worker',
        value: 'worker',
        align: 'center',
      },
      {
        text: 'Status',
        value: 'status',
      },
      {
        text: 'HIT',
        value: 'hit',
      },
    ],
    array_columns_selected_initial_general: [
      'id_assignment',
      'datetime_creation',
      'datetime_accept',
      'datetime_submit',
      'worker',
      'status',
      'hit',
    ],
    array_columns_selected_initial_finances: [
      'id_assignment',
      'datetime_creation',
      'datetime_accept',
      'datetime_submit',
      'worker',
      'status',
      'hit',
    ],
    array_columns_selected_general: null,
    array_columns_selected_finances: null,

    objectFiltersGeneral: null,
    objectFiltersFinances: null,
    objectFiltersDefaultGeneral: {
      show_only_submitted_assignments: false,
      assignmentsSelected: [],
      hitsSelected: [],
      batchesSelected: [],
      workersSelected: [],
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

    get_object_assignments_selected: state => state.object_assignments_selected,
    get_array_assignments: (state, getters, rootState) => (
      use_sandbox = undefined,
    ) => {
      if (use_sandbox == undefined) {
        return rootState.module_app.use_sandbox
          ? state.array_assignments_sandbox
          : state.array_assignments;
      }
      return use_sandbox
        ? state.array_assignments_sandbox
        : state.array_assignments;
    },
    get_object_assignments: (state, getters, rootState) => (
      use_sandbox = undefined,
    ) => {
      if (use_sandbox == undefined) {
        return rootState.module_app.use_sandbox
          ? state.object_assignments_sandbox
          : state.object_assignments;
      }
      return use_sandbox
        ? state.object_assignments_sandbox
        : state.object_assignments;
    },
    list_assignments: (state, getters) => {
      if (Object.keys(getters.get_object_assignments()).length == 0) {
        return [];
      }
      return _.orderBy(
        getters.get_object_assignments(),
        ['datetime_creation'],
        ['desc'],
      );
    },
    set_ids_worker: state => state.set_ids_worker,
  },
  mutations: {
    setPaginationGeneral(state, { pagination, setPageTo1 }) {
      setPagination({
        pagination,
        setPageTo1,
        namePagination: 'paginationGeneral',
        nameLocalStorage: 'pagination_assignments_general',
        state,
      });
    },
    setPaginationFinances(state, { pagination, setPageTo1 }) {
      setPagination({
        pagination,
        setPageTo1,
        namePagination: 'paginationFinances',
        nameLocalStorage: 'pagination_assignments_finances',
        state,
      });
    },
    set_array_columns_general(state, array_columns) {
      localforage.setItem('array_columns_assignments_general', array_columns);
      state.array_columns_selected_general = array_columns;
    },
    set_assignments(state, { data, use_sandbox }) {
      let array_assignments = null;
      if (use_sandbox) {
        state.array_assignments_sandbox = [];
        array_assignments = state.array_assignments_sandbox;
      } else {
        state.array_assignments = [];
        array_assignments = state.array_assignments;
      }

      _.forEach(data, (data) => {
        const assignment = new Assignment(data);
        Vue.set(array_assignments, array_assignments.length, assignment);
      });
    },
    // set_assignments(state, {data_assignments, object_hits, use_sandbox}) {
    //     let object_assignments = null;
    //     if(use_sandbox)
    //     {
    //         object_assignments = state.object_assignments_sandbox;
    //     } else {
    //         object_assignments = state.object_assignments;
    //     }
    //     // console.log('########')
    //     state.set_ids_worker = new Set();
    //
    //     _.forEach(data_batches, function(data_batch) {
    //         _.forEach(data_batch.hits, function(data_hit) {
    //         	const id_hit = data_hit.id;
    //         	const hit = object_hits[id_hit];
    //
    //
    //             _.forEach(data_hit.assignments, function(data_assignment) {
    //             	state.set_ids_worker.add(data_assignment.worker);
    //             	data_assignment.hit = hit;
    //             	// console.log(hit)
    // 	            const assignment = new Assignment(data_assignment);
    //             	// console.log(assignment)
    //
    // 	            Vue.set(object_assignments, assignment.id, assignment);
    //
    // 	            Vue.set(hit.object_assignments, assignment.id, assignment);
    //             });
    //         });
    //     });
    //     // console.log('########')
    //
    //     // console.log(state.set_ids_worker);
    // },
    clear_sandbox(state) {
      state.object_assignments_sandbox = {};
    },
    // append_assignments(state, {object_batches, data_batches, object_hits, use_sandbox}) {
    //           let object_assignments = null;
    //           if(use_sandbox)
    //           {
    //               object_assignments = state.object_assignments_sandbox;
    //           } else {
    //               object_assignments = state.object_assignments;
    //           }

    //           state.set_ids_worker = new Set();

    //           _.forEach(data_batches, function(data_batch) {
    //           	const id_batch = data_batch.id;
    //           	const batch = object_batches[id_batch];

    //               _.forEach(data_batch.hits, function(data_hit) {
    //            	const id_hit = data_hit.id;
    //            	const hit = object_hits[id_hit];

    //                _.forEach(data_hit.assignments, function(data_assignment) {
    //                	state.set_ids_worker.add(data_assignment.worker);
    //                	data_assignment.hit = hit;
    // 	            const assignment = new Assignment(data_assignment);

    // 	            Vue.set(object_assignments, assignment.id, assignment);

    // 	            Vue.set(hit.assignments, hit.assignments.length, assignment);
    //             });
    //               });
    //           });

    //           console.log(state.set_ids_worker);
    // },
    clear_assignments_selected(state) {
      state.object_assignments_selected = {};
    },
    set_assignments_selected(state, { array_items, add }) {
      if (add === true) {
        _.forEach(array_items, (item) => {
          Vue.set(state.object_assignments_selected, item.id, item.id);
        });
      } else {
        _.forEach(array_items, (item) => {
          Vue.delete(state.object_assignments_selected, item.id);
        });
      }
    },
    reset: (state) => {
      state.object_assignments = {};
      state.object_assignments_sandbox = {};
      state.set_ids_worker = null;
      state.object_assignments_selected = {};
    },
    set_urls(state, config) {
      state.url_api_projects_assignments = config.url_api_projects_assignments;
    },
  },
  actions: {
    async init({ state, commit, dispatch }) {
      await Promise.all([
        /**
         * init columns
         */
        dispatch('loadState', {
          nameLocalStorage: 'array_columns_assignments_general',
          nameState: 'array_columns_selected_general',
          objectStateDefault: state.array_columns_selected_initial_general,
        }),
        dispatch('loadState', {
          nameLocalStorage: 'array_columns_assignments_finances',
          nameState: 'array_columns_selected_finances',
          objectStateDefault: state.array_columns_selected_initial_finances,
        }),
        /**
         * init pagination
         */
        dispatch('loadState', {
          nameLocalStorage: 'pagination_assignments_general',
          nameState: 'paginationGeneral',
        }),
        dispatch('loadState', {
          nameLocalStorage: 'pagination_assignments_finances',
          nameState: 'paginationFinances',
        }),
        /**
         * init filters
         */
        dispatch('loadState', {
          nameLocalStorage: 'filtersAssignmentsGeneral',
          nameState: 'objectFiltersGeneral',
          objectStateDefault: state.objectFiltersDefaultGeneral,
        }),
        dispatch('loadState', {
          nameLocalStorage: 'filtersAssignmentsFinances',
          nameState: 'objectFiltersFinances',
          objectStateDefault: state.objectFiltersDefaultGeneral,
        }),
      ]);
    },
    reset_array_columns_general({ state, commit }) {
      commit(
        'set_array_columns_general',
        state.array_columns_selected_initial_general,
      );
    },
  },
});
