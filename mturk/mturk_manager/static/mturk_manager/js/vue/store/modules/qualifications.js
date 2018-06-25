import axios from 'axios';
import Vue from 'vue';
import _ from 'lodash';
import { Qualification } from '../../classes/qualifications.js';

export const moduleQualifications = {
	namespaced: true,
	state: {
        url_api_qualifications: undefined,
        // url_api_qualification: undefined,
        object_policies: null,
        object_policies_sandbox: null,
	},  
    getters: {
    	list_policies: (state, getters, rootState) => {
    		const object_current = rootState.use_sandbox ? state.object_policies_sandbox : state.object_policies;

    		if(object_current == null)
    		{
    			return [];
			}
            return _.orderBy(object_current, ['created_at'], ['desc']);
    	},
    	get_url_api_qualifications: (state, getters, rootState) => (value='') => {
    		let url = state.url_api_qualifications;

    		url += value;

    		if(!rootState.use_sandbox) {
    			url += '?use_sandbox=false&';
    		} else {
    			url += '?';
    		}
    		return url;
    	},
	},
	mutations: {
        set_url_api_qualifications(state, url_new) {
            state.url_api_qualifications = url_new;
        },
        // set_url_api_qualification(state, url_new) {
        //     state.url_api_qualification = url_new;
        // },
		set_qualificiations(state, data_policies) {
			state.object_policies = {};
        	_.forEach(data_policies, function(data_policy){
    			const obj_policy = new Qualification(data_policy);
    			Vue.set(state.object_policies, obj_policy.id_mturk, obj_policy);
        	});
		},
		set_qualificiations_sandbox(state, data_policies) {
			state.object_policies_sandbox = {};
        	_.forEach(data_policies, function(data_policy){
    			const obj_policy = new Qualification(data_policy);
    			Vue.set(state.object_policies_sandbox, obj_policy.id_mturk, obj_policy);
        	});
		},
		add_qualification(state, obj_policy) {
			Vue.set(state.object_policies, obj_policy.id_mturk, obj_policy);
		},
		add_qualification_sandbox(state, obj_policy) {
			Vue.set(state.object_policies_sandbox, obj_policy.id_mturk, obj_policy);
		},
		delete_qualifications(state, list_ids) {
        	_.forEach(list_ids, id => Vue.delete(state.object_policies, id) );
		},
		delete_qualifications_sandbox(state, list_ids) {
        	_.forEach(list_ids, id => Vue.delete(state.object_policies_sandbox, id) );
		},
		// delete_qualifications(state, obj_policy) {
		// 	Vue.set(state.object_policies, obj_policy.id, obj_policy);
		// },
	},
	actions: { 
		async sync_qualifications({commit, state, getters, rootState}, force=false) {
			const use_sandbox = rootState.use_sandbox;
    		const object_current = rootState.use_sandbox ? state.object_policies_sandbox : state.object_policies;
            if(object_current == null || force) {
				await axios.get(getters.get_url_api_qualifications())
			    .then(response => {
			    	if(use_sandbox) {
	                	commit('set_qualificiations_sandbox', response.data);
			    	} else {
	                	commit('set_qualificiations', response.data);
			    	}
			    })
			}
		},
		async update_qualification({commit, state, getters, rootState}, object_qualification) {
			const use_sandbox = rootState.use_sandbox;

			await axios.put(
				getters.get_url_api_qualifications(object_qualification.id_mturk),
				object_qualification.get_as_formdata(true),
				{
					headers: {"X-CSRFToken": rootState.token_csrf}
				}
			).then(response => {
		    	if(use_sandbox) {
                	commit('add_qualification_sandbox', new Qualification(response.data));
		    	} else {
                	commit('add_qualification', new Qualification(response.data));
		    	}
		    })

		},
		async add_qualification({commit, state, getters, rootState}, object_qualification) {
			const use_sandbox = rootState.use_sandbox;

			await axios.post(
				getters.get_url_api_qualifications(), 
				object_qualification.get_as_formdata(),
				{
					headers: {"X-CSRFToken": rootState.token_csrf}
				}
			).then(response => {
		    	if(use_sandbox) {
                	commit('add_qualification_sandbox', new Qualification(response.data));
		    	} else {
                	commit('add_qualification', new Qualification(response.data));
		    	}
		    })
		},
		async delete_qualifications({commit, state, getters, rootState}, list_qualifications) {
			const use_sandbox = rootState.use_sandbox;
			// const list_ids = list_qualifications.map(qualifiction => qualifiction.id_mturk)


			// _.forEach(list_qualifications, qualification => form_data.append('id_mturk[]', qualification.id_mturk))
			const list_ids = list_qualifications.map(qualifiction => qualifiction.id_mturk);

			const string_parameter = list_ids.map(id => 'ids=' + id).join('&');

			await axios.delete(
				getters.get_url_api_qualifications() + string_parameter, 
				{
					headers: {"X-CSRFToken": rootState.token_csrf}
				}
			).then(response => {
		    	if(use_sandbox) {
					commit('delete_qualifications_sandbox', list_ids);
		    	} else {
					commit('delete_qualifications', list_ids);
		    	}
                // commit('add_qualification', new Qualification(response.data));
		    })
		},
	},
}