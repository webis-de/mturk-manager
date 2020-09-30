import Vue from 'vue';
import _ from 'lodash';
import localforage from 'localforage';
import Worker from '../../classes/workers.js';
import { initFilters, initPagination, setPagination } from '../../helpers';
import baseModule from './base.module';

export const moduleWorkers = _.merge({}, baseModule, {
  state: {
    url_api_workers: undefined,
    object_workers: {},
    object_workers_sandbox: {},

    arrayWorkers: null,
    arrayWorkersSandbox: null,

    object_workers_selected: {},

    url_api_global_db: undefined,
    // loaded_status_block: false,
    // loaded_status_block_sandbox: false,

    paginationGeneral: {
      itemsPerPage: 25,
      sortBy: ['id_worker'],
      sortDesc: [true],
    },

    array_columns_general: [
      {
        text: 'Name',
        value: 'id_worker',
        class: ['text-center'],
      },
      {
        text: 'Assignments',
        value: 'number_of_assignments',
        align: 'center',
        width: '1px',
        class: ['text-no-wrap'],
      },
      {
        text: 'Approved',
        value: 'number_of_approved_assignments_of_project',
        align: 'center',
        width: '1px',
        class: ['text-no-wrap'],
      },
      {
        text: 'Rejected',
        value: 'number_of_rejected_assignments_of_project',
        align: 'center',
        width: '1px',
        class: ['text-no-wrap'],
      },
      {
        text: 'Ratio Approved',
        value: 'ratio_approved_assignments_of_project',
        align: 'center',
        width: '1px',
        class: ['text-no-wrap'],
      },
      {
        text: 'Approved (global)',
        value: 'number_of_approved_assignments',
        align: 'center',
        width: '1px',
        class: ['text-no-wrap'],
      },
      {
        text: 'Rejected (global)',
        value: 'number_of_rejected_assignments',
        align: 'center',
        width: '1px',
        class: ['text-no-wrap'],
      },
      {
        text: 'Ratio Approved (global)',
        value: 'ratio_approved_assignments',
        align: 'center',
        width: '1px',
        class: ['text-no-wrap'],
      },
      {
        text: 'Assignment Limit',
        value: 'counter_assignments',
        align: 'center',
        width: '1px',
        sortable: false,
        class: ['text-no-wrap'],
      },
      {
        text: 'Project Block',
        value: 'block_soft',
        width: '1px',
        sortable: false,
        class: ['text-no-wrap'],
      },
      {
        text: 'Soft MTurk Block',
        value: 'block_soft_hard',
        width: '1px',
        sortable: false,
        class: ['text-no-wrap'],
      },
      {
        text: 'Hard MTurk Block',
        value: 'block_hard',
        width: '1px',
        sortable: false,
        class: ['text-no-wrap'],
      },
    ],
    objectColumnsSelectedGeneral: null,
    objectColumnsSelectedInitialGeneral: {
      id_worker: true,
      number_of_assignments: true,
      number_of_approved_assignments_of_project: true,
      number_of_rejected_assignments_of_project: true,
      ratio_approved_assignments_of_project: true,
      number_of_approved_assignments: true,
      number_of_rejected_assignments: true,
      ratio_approved_assignments: true,
      counter_assignments: true,
      block_soft: true,
      block_soft_hard: true,
      block_hard: true,
    },
    objectFiltersGeneral: null,
    objectFiltersDefaultGeneral: {
      workersSelected: [],
      batchesSelected: [],
      statesBlock: [],
    },
  },
  getters: {
    get_object_workers_selected: (state) => state.object_workers_selected,
    get_array_columns_general: (state) => state.array_columns_general,
    get_array_columns_selected_general: (state) => {
      if (state.array_columns_selected_general === null) {
        return state.array_columns_selected_initial_general;
      }
      return state.array_columns_selected_general;
    },
    // get_object_workers: (state, getters, rootState) => {
    get_object_workers: (state, getters, rootState) => (
      use_sandbox = undefined,
    ) => {
      if (use_sandbox == undefined) {
        return rootState.module_app.use_sandbox
          ? state.object_workers_sandbox
          : state.object_workers;
      }
      return use_sandbox
        ? state.object_workers_sandbox
        : state.object_workers;
    },
    get_array_workers: (state, getters, rootState) => (
      use_sandbox = undefined,
    ) => {
      if (use_sandbox === undefined) {
        return rootState.module_app.use_sandbox
          ? state.array_workers_sandbox
          : state.array_workers;
      }
      return use_sandbox ? state.array_workers_sandbox : state.array_workers;
    },
    list_workers: (state, getters, rootState) => {
      // console.log('done')
      // const object_current = rootState.module_app.use_sandbox ? state.object_workers_sandbox : state.object_workers;
      // console.log(state.object_workers_sandbox)
      if (getters.get_object_workers() == null) {
        return [];
        // return {};
      }
      return _.values(getters.get_object_workers());
      // return _.orderBy(object_current, ['created_at'], ['desc']);
    },
  },
  mutations: {
    setItemsSelected(state, { items }) {
      state.object_workers_selected = items;
    },
    // setPaginationGeneral(state, { pagination, setPageTo1 }) {
    //   setPagination({
    //     pagination,
    //     setPageTo1,
    //     namePagination: 'paginationGeneral',
    //     nameLocalStorage: 'pagination_workers_general',
    //     state,
    //   });
    // },
    // set_array_columns_general(state, array_columns) {
    //   localforage.setItem('array_columns_workers_general', array_columns);
    //   state.array_columns_selected_general = array_columns;
    // },
    clear_workers_selected(state) {
      state.object_workers_selected = {};
    },
    set_workers_selected(state, { array_items, add }) {
      if (add === true) {
        _.forEach(array_items, (item) => {
          Vue.set(state.object_workers_selected, item.id, item.id);
        });
      } else {
        _.forEach(array_items, (item) => {
          Vue.delete(state.object_workers_selected, item.id);
        });
      }
    },
    set_urls(state, paths) {
      state.url_api_workers = paths.url_api_workers;
      state.url_api_workers_get_blocks_hard = paths.url_api_workers_get_blocks_hard;
    },
    // set_url_api_global_db(state, url_new) {
    //     state.url_api_global_db = url_new;
    // },
    update_worker(state, { data_worker, use_sandbox }) {
      let object_workers = null;
      if (use_sandbox) {
        object_workers = state.object_workers_sandbox;
      } else {
        object_workers = state.object_workers;
      }

      const obj_worker = new Worker(data_worker);
      Vue.set(object_workers, obj_worker.id_worker, obj_worker);
    },
    set_worker(state, { worker, worker_new, array_fields }) {
      _.forEach(array_fields, (name_field) => {
        Vue.set(worker, name_field, worker_new[name_field]);
      });
    },
    // update_worker_count_assignments_limit(state, {worker, value, use_sandbox}) {
    // 	let object_workers = null;
    // 	if(use_sandbox)
    // 	{
    // 		object_workers = state.object_workers_sandbox;
    // 	} else {
    // 		object_workers = state.object_workers;
    // 	}

    // 	Vue.set(object_workers[worker.name], 'count_assignments_limit', value);
    // },
    update_status_block_soft(state, { worker, data, use_sandbox }) {
      let object_workers = null;
      if (use_sandbox) {
        object_workers = state.object_workers_sandbox;
      } else {
        object_workers = state.object_workers;
      }

      Vue.set(worker, 'is_blocked_soft', data.is_blocked_soft);
    },
    update_status_block_hard(state, { worker, data, use_sandbox }) {
      let array_workers = null;
      if (use_sandbox) {
        array_workers = state.array_workers_sandbox;
      } else {
        array_workers = state.array_workers;
      }

      Vue.set(worker, 'is_blocked_hard', data.is_blocked_hard);
    },
    update_status_block_global(state, { worker, data, use_sandbox }) {
      let object_workers = null;
      if (use_sandbox) {
        object_workers = state.object_workers_sandbox;
      } else {
        object_workers = state.object_workers;
      }

      Vue.set(worker, 'is_blocked_global', data.is_blocked_global);
    },
    // update_worker_sandbox(state, data_worker) {
    // 	const obj_worker = new Worker(data_worker);
    // 	Vue.set(state.object_workers_sandbox, obj_worker.name, obj_worker);
    // },
    set_workers(state, { data, use_sandbox }) {
      let array_workers = null;
      if (use_sandbox) {
        state.array_workers_sandbox = [];
        array_workers = state.array_workers_sandbox;
      } else {
        state.array_workers = [];
        array_workers = state.array_workers;
      }

      _.forEach(data, (data_worker) => {
        const obj_worker = new Worker(data_worker);
        Vue.set(array_workers, array_workers.length, obj_worker);
      });
    },
    append_workers(state, { data_workers, use_sandbox }) {
      let object_workers = null;
      if (use_sandbox) {
        object_workers = state.object_workers_sandbox;
      } else {
        object_workers = state.object_workers;
      }

      _.forEach(data_workers, (data_worker) => {
        const obj_worker = new Worker(data_worker);
        Vue.set(object_workers, obj_worker.id, obj_worker);
      });
    },
    // set_workers(state, {data_workers, use_sandbox}) {
    // 	let object_workers = null;
    // 	if(use_sandbox)
    // 	{
    // 		state.object_workers_sandbox = {};
    // 		object_workers = state.object_workers_sandbox;
    // 	} else {
    // 		state.object_workers = {};
    // 		object_workers = state.object_workers;
    // 	}

    //       	_.forEach(data_workers, function(data_worker){
    //   			const obj_worker = new Worker(data_worker);
    //   			Vue.set(object_workers, obj_worker.name, obj_worker);
    //       	});
    // },
    set_blocks_hard(state, { data, use_sandbox }) {
      const set_workers_blocked = new Set(data);

      let array_workers = null;
      if (use_sandbox) {
        array_workers = state.arrayWorkersSandbox;
      } else {
        array_workers = state.arrayWorkers;
      }
      _.forEach(array_workers, (worker) => {
        Vue.set(worker, 'is_blocked_hard', set_workers_blocked.has(worker.id));
      });
    },
    set_data_global_db(state, { data, use_sandbox }) {
      const data_status_block = data.blocks;
      const object_counters = data.counters;

      const set_blocked_soft = new Set(data_status_block.soft);
      const set_blocked_hard = new Set(data_status_block.hard);

      let object_workers = null;
      if (use_sandbox) {
        object_workers = state.object_workers_sandbox;
      } else {
        object_workers = state.object_workers;
      }

      _.forEach(object_workers, (worker) => {
        if (set_blocked_soft.has(worker.id_worker)) {
          Vue.set(worker, 'is_blocked_soft', true);
        } else {
          Vue.set(worker, 'is_blocked_soft', false);
        }

        if (set_blocked_hard.has(worker.id_worker)) {
          Vue.set(worker, 'is_blocked_hard', true);
        } else {
          Vue.set(worker, 'is_blocked_hard', false);
        }

        if (object_counters.hasOwnProperty(worker.id_worker)) {
          Vue.set(
            worker,
            'count_assignments_limit',
            object_counters[worker.id_worker],
          );
        } else {
          Vue.set(worker, 'count_assignments_limit', 0);
        }
      });
    },
    clear_sandbox(state) {
      state.object_workers_sandbox = {};
    },
    reset: (state) => {
      state.object_workers = {};
      state.object_workers_sandbox = {};
    },
  },
  actions: {
    async init({ state, commit, dispatch }) {
      await Promise.all([
        /**
         * init columns
         */
        dispatch('loadState', {
          nameLocalStorage: 'array_columns_workers_general',
          nameState: 'array_columns_selected_general',
          objectStateDefault: state.array_columns_selected_initial_general,
        }),
        /**
         * init pagination
         */
        dispatch('loadState', {
          nameLocalStorage: 'pagination_workers_general',
          nameState: 'paginationGeneral',
        }),
        /**
         * init filters
         */
        dispatch('loadState', {
          nameLocalStorage: 'filtersWorkersGeneral',
          nameState: 'objectFiltersGeneral',
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
        state.array_columns_selected_initial_general,
      );
    },
    // async sync_workers({commit, state, getters, rootState, rootGetters}, force=false) {
    // 	const use_sandbox = rootState.module_app.use_sandbox;

    //           if(getters.get_object_workers(use_sandbox) == null || force) {
    // 		await axios.get(rootGetters.getUrlApi(state.url_api_workers, use_sandbox))
    // 	    .then(response => {
    //               	commit('set_workers', {'data_workers': response.data, use_sandbox});
    // 	    })

    // 		await axios.get(rootGetters.getUrlApi(state.url_api_global_db, use_sandbox))
    // 	    .then(response => {
    //               	commit('set_data_global_db', {'data': response.data, use_sandbox});
    // 	    })
    // 	}
    // },
    // async update_status_block({commit, state, getters, rootState, rootGetters}, {worker, status_block_new, status_block_old}) {
    // 	const use_sandbox = rootState.module_app.use_sandbox;

    //           const response = await dispatch('makeRequest', {
    //               method: 'patch',
    //               url: rootGetters.getUrlApi({
    //                   url: state.url_api_workers,
    //                   use_sandbox,
    //               }),
    //               data: Array.from(list_ids),
    //           }, { root: true });

    // 	const form_data = new FormData();
    // 	form_data.set('is_blocked', JSON.stringify({
    // 		status_block_new,
    // 		status_block_old,
    // 	}));

    // 	await axios.put(
    // 		rootGetters.getUrlApi(state.url_api_workers, use_sandbox, worker.name),
    // 		form_data,
    // 		{
    // 			headers: {"X-CSRFToken": rootState.token_csrf}
    // 		},
    // 	)
    //     .then(response => {
    //     	// if(rootState.module_app.use_sandbox) {
    //      //      		commit('update_worker_sandbox', response.data);
    //     	// } else {
    //           	commit('update_worker_status_block', {worker, status_block_new, use_sandbox});
    //     	// }
    //     })
    // },
  },
});
