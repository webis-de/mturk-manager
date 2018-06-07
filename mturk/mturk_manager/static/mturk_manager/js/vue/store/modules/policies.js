import axios from 'axios';
import Vue from 'vue';
import _ from 'lodash';

export const modulePolicies = {
	namespaced: true,
	state: {
        url_api_policies: undefined,
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
        set_url_api_policies(state, url_new) {
            state.url_api_policies = url_new;
        },
		set_policies(state, data_policies) {
			state.object_policies = {};
        	_.forEach(data_policies, function(data_policy){
    			const obj_policy = new Policy(data_policy);
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
				await axios.get(state.url_api_policies)
			    .then(response => {
	                commit('set_policies', response.data);
			    })
			}
		},
		async add_policy({commit, state}, obj_policy) {
			console.log(obj_policy.get_as_formdata())
			const token = document.cookie.match(new RegExp('csrftoken=([^;]+)'))[1]

			await axios.post(
				state.url_api_policies, 
				obj_policy.get_as_formdata(),
				{
					headers: {"X-CSRFToken": token}
				}
			).then(response => {
                commit('add_policy', new Policy(response.data));
		    })
		},
		async update_policy({commit, state}, obj_policy) {
			console.log(obj_policy.get_as_formdata())
			const token = document.cookie.match(new RegExp('csrftoken=([^;]+)'))[1]

			await axios.put(
				state.url_api_policies, 
				obj_policy.get_as_formdata(),
				{
					headers: {"X-CSRFToken": token}
				}
			).then(response => {
                // commit('add_policy', new Policy(response.data));
		    })
		},
	},
}

export class Policy {
	constructor(data) {
		this.id = data.QualificationTypeId;
		// this.created_at = new Date(data.CreationTime);
		this.description = data.Description;
		this.is_requestable = data.IsRequestable;
		this.name = data.Name;
		this.status = data.QualificationTypeStatus;
	}

	get_as_formdata() {
		const form_data = new FormData();
		form_data.set('id', this.id);
		form_data.set('created_at', this.created_at);
		form_data.set('description', this.description);
		form_data.set('is_requestable', this.is_requestable);
		form_data.set('name', this.name);
		form_data.set('status', this.status);

		return form_data;
		return {
			id: this.id,
			created_at: this.created_at,
			description: this.description,
			is_requestable: this.is_requestable,
			name: this.name,
			status: this.status,
		};
	}
}