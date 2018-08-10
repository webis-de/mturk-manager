import axios from 'axios';
import Vue from 'vue';
import _ from 'lodash';
import { Worker } from '../../classes/workers.js';
import { STATUS_BLOCK } from '../../classes/enums.js';

export const moduleWorkers = {
	namespaced: true,
	state: {
        url_api_workers: undefined,
        object_workers: null,
        object_workers_sandbox: null,
        
        url_api_status_block: undefined,
        // loaded_status_block: false,
        // loaded_status_block_sandbox: false,
	},  
    getters: {
    	// get_object_workers: (state, getters, rootState) => {
    	get_object_workers: (state, getters, rootState) => (use_sandbox=undefined) => {
    		if(use_sandbox == undefined)
    		{
    			return rootState.use_sandbox ? state.object_workers_sandbox : state.object_workers;
    		} else {
    			return use_sandbox ? state.object_workers_sandbox : state.object_workers;
    		}
    	},
    	list_workers: (state, getters, rootState) => {
    		// console.log('done')
    		// const object_current = rootState.use_sandbox ? state.object_workers_sandbox : state.object_workers;
    		// console.log(state.object_workers_sandbox)
    		if(getters.get_object_workers() == null)
    		{
    			return [];
    			// return {};
			}
            return _.values(getters.get_object_workers());
            // return _.orderBy(object_current, ['created_at'], ['desc']);
    	},
	},
	mutations: {
        set_url_api_workers(state, url_new) {
            state.url_api_workers = url_new;
        },
        set_url_api_status_block(state, url_new) {
            state.url_api_status_block = url_new;
        },
		update_worker(state, {data_worker, use_sandbox}) {
			let object_workers = null;
			if(use_sandbox)
			{
				object_workers = state.object_workers_sandbox;
			} else {
				object_workers = state.object_workers;
			}

			const obj_worker = new Worker(data_worker);
			Vue.set(object_workers, obj_worker.name, obj_worker);
		},
		update_worker_status_block(state, {worker, status_block_new, use_sandbox}) {
			let object_workers = null;
			if(use_sandbox)
			{
				object_workers = state.object_workers_sandbox;
			} else {
				object_workers = state.object_workers;
			}

			Vue.set(object_workers[worker.name], 'is_blocked', status_block_new);
		},
		// update_worker_sandbox(state, data_worker) {
		// 	const obj_worker = new Worker(data_worker);
		// 	Vue.set(state.object_workers_sandbox, obj_worker.name, obj_worker);
		// },
		set_workers(state, {data_workers, use_sandbox}) {
			let object_workers = null;
			if(use_sandbox)
			{
				state.object_workers_sandbox = {};
				object_workers = state.object_workers_sandbox;
			} else {
				state.object_workers = {};
				object_workers = state.object_workers;
			}

        	_.forEach(data_workers, function(data_worker){
    			const obj_worker = new Worker(data_worker);
    			Vue.set(object_workers, obj_worker.name, obj_worker);
        	});
		},
		set_status_block(state, {data_status_block, use_sandbox}) {
			const set_blocked_soft = new Set(data_status_block.soft);
			const set_blocked_hard = new Set(data_status_block.hard);

			let object_workers = null;
			if(use_sandbox)
			{
				object_workers = state.object_workers_sandbox;
			} else {
				object_workers = state.object_workers;
			}
			
			_.forEach(object_workers, (worker) => {
				if(set_blocked_soft.has(worker.name))
				{
					Vue.set(worker, 'is_blocked', STATUS_BLOCK.SOFT);
				} else if(set_blocked_hard.has(worker.name)) {
					Vue.set(worker, 'is_blocked', STATUS_BLOCK.HARD);
				} else {
					Vue.set(worker, 'is_blocked', STATUS_BLOCK.NONE);
				}
			});
		},
	},
	actions: {
		async sync_workers({commit, state, getters, rootState, rootGetters}, force=false) {
			const use_sandbox = rootState.use_sandbox;

            if(getters.get_object_workers(use_sandbox) == null || force) {
				await axios.get(rootGetters.get_url_api(state.url_api_workers, use_sandbox))
			    .then(response => {
                	commit('set_workers', {'data_workers': response.data, use_sandbox});
			    })

				await axios.get(rootGetters.get_url_api(state.url_api_status_block, use_sandbox))
			    .then(response => {
                	commit('set_status_block', {'data_status_block': response.data, use_sandbox});
			    })
			}


		},
		async update_status_block({commit, state, getters, rootState, rootGetters}, {worker, status_block_new, status_block_old}) {
			const use_sandbox = rootState.use_sandbox;

			const form_data = new FormData();
			form_data.set('is_blocked', JSON.stringify({
				status_block_new,
				status_block_old,
			}));

			await axios.put(
				rootGetters.get_url_api(state.url_api_workers, use_sandbox, worker.name),
				form_data,
				{
					headers: {"X-CSRFToken": rootState.token_csrf}
				},
			)
		    .then(response => {
		    	// if(rootState.use_sandbox) {
       //      		commit('update_worker_sandbox', response.data);
		    	// } else {
            	commit('update_worker_status_block', {worker, status_block_new, use_sandbox});
		    	// }
		    })
		},
	},
}