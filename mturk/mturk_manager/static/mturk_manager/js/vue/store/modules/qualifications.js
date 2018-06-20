import axios from 'axios';
import Vue from 'vue';
import _ from 'lodash';
import { Qualification } from '../../classes/qualifications.js';

export const moduleQualifications = {
	namespaced: true,
	state: {
        url_api_qualifications: undefined,
        url_api_qualification: undefined,
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
        set_url_api_qualification(state, url_new) {
            state.url_api_qualification = url_new;
        },
		set_qualificiations(state, data_policies) {
			state.object_policies = {};
        	_.forEach(data_policies, function(data_policy){
    			const obj_policy = new Qualification(data_policy);
    			Vue.set(state.object_policies, obj_policy.id_mturk, obj_policy);
        	});
		},
		add_qualification(state, obj_policy) {
			Vue.set(state.object_policies, obj_policy.id, obj_policy);
		},
		delete_qualifications(state, list_ids) {
        	_.forEach(list_ids, id => Vue.delete(state.object_policies, id) );
		},
		// delete_qualifications(state, obj_policy) {
		// 	Vue.set(state.object_policies, obj_policy.id, obj_policy);
		// },
	},
	actions: {
		async sync_qualifications({commit, state}, force=false) {
            if(state.object_policies == null || force) {
				await axios.get(state.url_api_qualifications)
			    .then(response => {
	                commit('set_qualificiations', response.data);
			    })
			}
		},
		async add_qualification({commit, state}, object_qualification) {
			console.log(object_qualification.get_as_formdata())
			const token = document.cookie.match(new RegExp('csrftoken=([^;]+)'))[1]

			await axios.post(
				state.url_api_qualifications, 
				object_qualification.get_as_formdata(),
				{
					headers: {"X-CSRFToken": token}
				}
			).then(response => {
                commit('add_qualification', new Qualification(response.data));
		    })
		},
		async delete_qualifications({commit, state}, list_qualifications) {
			const token = document.cookie.match(new RegExp('csrftoken=([^;]+)'))[1]
			// const list_ids = list_qualifications.map(qualifiction => qualifiction.id_mturk)


			// _.forEach(list_qualifications, qualification => form_data.append('id_mturk[]', qualification.id_mturk))
			const list_ids = list_qualifications.map(qualifiction => qualifiction.id_mturk);

			const string_parameter = '?' + list_ids.map(id => 'ids=' + id).join('&');

			await axios.delete(
				state.url_api_qualifications + string_parameter, 
				{
					headers: {"X-CSRFToken": token}
				}
			).then(response => {
				commit('delete_qualifications', list_ids);
                // commit('add_qualification', new Qualification(response.data));
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