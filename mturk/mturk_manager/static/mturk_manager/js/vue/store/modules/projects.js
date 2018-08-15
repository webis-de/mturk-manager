import Vue from 'vue';
import axios from 'axios';
import _ from 'lodash';
import { Project } from '../../classes/project.js';

export const moduleProjects = {
	namespaced: true,
	state: {
		object_projects: null,
		slug_project_current: null,
        url_api_projects: undefined,
	},
	getters: {
		get_project_current(state) {
			return state.object_projects[state.slug_project_current];
		},
    	get_object_project: (state, getters, rootState) => {
    		console.log(rootState.name_project)
			return state.object_projects;
    	},
    	get_object_projects: (state) => {
			return state.object_projects;
    	},
	},
	mutations: {
        set_slug_project_current(state, slug_project_current) {
            state.slug_project_current = slug_project_current;
        },
        set_url_api_projects(state, url_new) {
            state.url_api_projects = url_new;
        },
        set_projects(state, data_projects) {
        	state.object_projects= {};
        	
        	_.forEach(data_projects, function(data_project){
    			const object_project = new Project(data_project);
    			Vue.set(state.object_projects, object_project.slug, object_project);
        	});
        },
	},
	actions: {
        async load_projects({state, commit, getters, rootGetters, dispatch}) {
            if(getters.get_object_projects == null) {
				await axios.get(rootGetters.get_url_api(state.url_api_projects, false))
			    .then(response => {
			    	console.log(response.data)
                	commit('set_projects', response.data);
			    })

				// await axios.get(rootGetters.get_url_api(state.url_api_status_block, use_sandbox))
			 //    .then(response => {
    //             	commit('set_status_block', {'data_status_block': response.data, use_sandbox});
			 //    })
			}
        },
	},
}