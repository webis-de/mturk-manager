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
    url_api_assignments: undefined,

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
      {
        text: 'Actions',
        value: 'actions',
        sortable: false,
        width: '10%',
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
      'actions',
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
    updateItem(state, { item }) {
      const nameState = 'array_assignments_sandbox';

      Vue.set(
        state[nameState],
        _.findIndex(state[nameState], itemOld => itemOld.id === item.id),
        item,
      );
    },
    set_array_columns_general(state, array_columns) {
      localforage.setItem('array_columns_assignments_general', array_columns);
      state.array_columns_selected_general = array_columns;
    },
    set_assignments(state, { data, use_sandbox }) {
      let arrayAssignments = null;
      if (use_sandbox) {
        state.array_assignments_sandbox = [];
        arrayAssignments = state.array_assignments_sandbox;
      } else {
        state.array_assignments = [];
        arrayAssignments = state.array_assignments;
      }

      _.forEach(data, (data) => {
        const assignment = new Assignment(data);
        Vue.set(arrayAssignments, arrayAssignments.length, assignment);
      });
    },
    clear_sandbox(state) {
      state.object_assignments_sandbox = {};
    },
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
      state.url_api_assignments = config.url_api_assignments;
    },
    update(state, { assignment }) {
      let item = _.find(state.array_assignments, item => item.id === assignment.id);
      if (item === undefined) {
        item = _.find(state.array_assignments_sandbox, item => item.id === assignment.id);
      }

      Vue.set(
        item,
        'status_external',
        assignment.status_external,
      );
      Vue.set(
        item,
        'status_internal',
        assignment.status_internal,
      );
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
    async updateItem({ commit }, { item }) {
      commit('updateItem', {
        item,
      });
    },
  },
});
