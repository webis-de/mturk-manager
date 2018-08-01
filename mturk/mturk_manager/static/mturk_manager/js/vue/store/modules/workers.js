import axios from 'axios';
import Vue from 'vue';
import _ from 'lodash';
import { Worker } from '../../classes/workers.js';

export const moduleWorkers = {
	namespaced: true,
	state: {
        url_api_workers: undefined,
        object_workers: null,
        object_workers_sandbox: null,
	},  
    getters: {
    	get_object_workers: (state, getters, rootState) => {
    		return rootState.use_sandbox ? state.object_workers_sandbox : state.object_workers;
    	},
    	list_workers: (state, getters, rootState) => {
    		// console.log('done')
    		// const object_current = rootState.use_sandbox ? state.object_workers_sandbox : state.object_workers;
    		// console.log(state.object_workers_sandbox)
    		if(getters.get_object_workers == null)
    		{
    			return [];
    			// return {};
			}
			// console.log(object_current)
            return _.values(getters.get_object_workers);
            // return _.orderBy(object_current, ['created_at'], ['desc']);
    	},
	},
	mutations: {
        set_url_api_workers(state, url_new) {
            state.url_api_workers = url_new;
        },
		update_worker(state, data_worker) {
			const obj_worker = new Worker(data_worker);
			Vue.set(state.object_workers, obj_worker.name, obj_worker);
		},
		update_worker_sandbox(state, data_worker) {
			const obj_worker = new Worker(data_worker);
			Vue.set(state.object_workers_sandbox, obj_worker.name, obj_worker);
		},
		set_workers(state, data_workers) {
			state.object_workers = {};
        	_.forEach(data_workers, function(data_worker){
    			const obj_worker = new Worker(data_worker);
    			Vue.set(state.object_workers, obj_worker.name, obj_worker);
        	});
		},
		set_workers_sandbox(state, data_workers) {
			state.object_workers_sandbox = {};
        	_.forEach(data_workers, function(data_worker){
    			const obj_worker = new Worker(data_worker);
    			Vue.set(state.object_workers_sandbox, obj_worker.name, obj_worker);
        	});
		},
	},
	actions: {
		async sync_workers({commit, state, getters, rootState, rootGetters}, force=false) {
            if(getters.get_object_workers == null || force) {
				await axios.get(rootGetters.get_url_api(state.url_api_workers))
			    .then(response => {
			    	if(rootState.use_sandbox) {
	                	commit('set_workers_sandbox', response.data);
			    	} else {
	                	commit('set_workers', response.data);
			    	}
			    })
			}
		},
		async update_status_block({commit, state, getters, rootState, rootGetters}, {worker, status_block_new}) {
			const form_data = new FormData();
			form_data.set('is_blocked', status_block_new);

			await axios.put(
				rootGetters.get_url_api(state.url_api_workers, worker.name),
				form_data,
				{
					headers: {"X-CSRFToken": rootState.token_csrf}
				},
			)
		    .then(response => {
		    	if(rootState.use_sandbox) {
                	commit('update_worker_sandbox', response.data);
		    	} else {
                	commit('update_worker', response.data);
		    	}
		    })
		},
	},
}