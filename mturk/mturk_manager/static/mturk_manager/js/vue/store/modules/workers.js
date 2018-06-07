import axios from 'axios';
import Vue from 'vue';
import _ from 'lodash';

export const moduleWorkers = {
	namespaced: true,
	state: {
        url_api_workers: undefined,
        object_workers: null,
	},  
    getters: {
    	list_workers: state => {
    		if(state.object_workers == null)
    		{
    			return [];
			}
			console.log(state.object_workers)
            return _.values(state.object_workers);
            // return _.orderBy(state.object_workers, ['created_at'], ['desc']);
    	},
	},
	mutations: {
        set_url_api_workers(state, url_new) {
            state.url_api_workers = url_new;
        },
		set_workers(state, data_workers) {
			state.object_workers = {};
        	_.forEach(data_workers, function(data_worker){
    			const obj_worker = new Worker(data_worker);
    			Vue.set(state.object_workers, obj_worker.name, obj_worker);
        	});
        	console.log(state.object_workers)
		},
	},
	actions: {
		async sync_workers({commit, state}, force=false) {
            if(state.object_policies == null || force) {
				await axios.get(state.url_api_workers)
			    .then(response => {
	                commit('set_workers', response.data.workers);
			    })
			}
		},
	},
}

export class Worker {
	constructor(data) {
		// this.m_id = data.QualificationTypeId;
		// this.m_created_at = new Date(data.CreationTime);
		// this.m_description = data.Description;
		// this.m_is_requestable = data.IsRequestable;
		this.name = data.name;
		// this.m_status = data.QualificationTypeStatus;
	}

	get_as_formdata() {
		const form_data = new FormData();
		// form_data.set('id', this.m_id);
		// form_data.set('created_at', this.m_created_at);
		// form_data.set('description', this.m_description);
		// form_data.set('is_requestable', this.m_is_requestable);
		form_data.set('name', this.name);
		// form_data.set('status', this.m_status);

		return form_data;
		return {
			id: this.m_id,
			created_at: this.m_created_at,
			description: this.m_description,
			is_requestable: this.m_is_requestable,
			name: this.name,
			status: this.m_status,
		};
	}

	// get_description() {
	// 	return this.m_description;
	// } 
	// get_is_requestable() {
	// 	return this.m_is_requestable;
	// } 
	// get_status() {
	// 	return this.m_status;
	// } 
}