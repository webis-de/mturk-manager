import axios from 'axios';
import Vue from 'vue';
import _ from 'lodash';
import { Qualification } from '../../classes/qualifications.js';

export const moduleQualifications = {
	namespaced: true,
	state: {
        url_api_qualifications: undefined,
        object_policies: null,
	},  
    getters: {
    	list_policies: state => {
    		if(state.object_policies == null)
    		{
    			return [];
			}

            return _.orderBy(state.object_policies, ['created_at'], ['desc']);
    	},
	},
	mutations: {
        set_url_api_qualifications(state, url_new) {
            state.url_api_qualifications = url_new;
        },
		set_policies(state, data_policies) {
			state.object_policies = {};
        	_.forEach(data_policies, function(data_policy){
    			const obj_policy = new Qualification(data_policy);
    			Vue.set(state.object_policies, obj_policy.id, obj_policy);
        	});
		},
		add_policy(state, obj_policy) {
			Vue.set(state.object_policies, obj_policy.id, obj_policy);
		},
	},
	actions: {
		async sync_policies({commit, state}, force=false) {
            if(state.object_policies == null || force) {
				await axios.get(state.url_api_qualifications)
			    .then(response => {
	                commit('set_policies', response.data);
			    })
			}
		},
		async add_policy({commit, state}, obj_policy) {
			console.log(obj_policy.get_as_formdata())
			const token = document.cookie.match(new RegExp('csrftoken=([^;]+)'))[1]

			await axios.post(
				state.url_api_qualifications, 
				obj_policy.get_as_formdata(),
				{
					headers: {"X-CSRFToken": token}
				}
			).then(response => {
                commit('add_policy', new Qualification(response.data));
		    })
		},
		async update_policy({commit, state}, obj_policy) {
			console.log(obj_policy.get_as_formdata())
			const token = document.cookie.match(new RegExp('csrftoken=([^;]+)'))[1]

			await axios.put(
				state.url_api_qualifications, 
				obj_policy.get_as_formdata(),
				{
					headers: {"X-CSRFToken": token}
				}
			).then(response => {
                // commit('add_policy', new Qualification(response.data));
		    })
		},
	},
}