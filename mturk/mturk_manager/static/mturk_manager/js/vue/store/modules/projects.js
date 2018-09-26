import Vue from 'vue';
import axios from 'axios';
import _ from 'lodash';
import Project from '../../classes/project';
import Settings_Batch from '../../classes/settings_batch';
import Template_Worker from '../../classes/template_worker';

export const moduleProjects = {
	namespaced: true,
	state: {
		object_projects: null,
		slug_project_current: null,

        url_api_projects: undefined,
        url_api_projects_check_uniqueness: undefined,
        url_api_projects_settings_batch: undefined,
        url_api_projects_templates_worker: undefined,
	},
	getters: {
		get_project_current(state) {
			return state.object_projects[state.slug_project_current];
		},
   //  	get_object_project: (state, getters, rootState) => {
   //  		console.log(rootState.name_project)
			// return state.object_projects;
   //  	},
    	get_object_projects: (state) => {
			return state.object_projects;
    	},
		get_slug_project_current(state) {
			return state.slug_project_current;
		},
	},
	mutations: {
        edit_project(state, data) {
        	const project = new Project(data);
        	Vue.set(state.object_projects, project.slug, project);
        }, 
        set_slug_project_current(state, slug_project_current) {
            state.slug_project_current = slug_project_current;
        },
        set_urls(state, config) {
            state.url_api_projects = config.url_api_projects;
            state.url_api_projects_check_uniqueness = config.url_api_projects_check_uniqueness;
            state.url_api_projects_settings_batch = config.url_api_projects_settings_batch;
            state.url_api_projects_templates_worker = config.url_api_projects_templates_worker;
        },
        set_settings_batch(state, {data, project}) {
            project.settings_batch = {};

            _.forEach(data, function(data_settings_batch) {
                const object_settings_batch = new Settings_Batch(data_settings_batch);
                Vue.set(project.settings_batch, object_settings_batch.id, object_settings_batch);
            });
        },
        set_templates_worker(state, {data, project}) {
        	project.templates_worker = {};

        	_.forEach(data, function(data_templates_worker) {
    			const object_template_worker = new Template_Worker(data_templates_worker);
    			Vue.set(project.templates_worker, object_template_worker.id, object_template_worker);
        	});
        },
        set_projects(state, data_projects) {
            state.object_projects= {};
            
            _.forEach(data_projects, function(data_project){
                const object_project = new Project(data_project);
                Vue.set(state.object_projects, object_project.slug, object_project);
            });
        },
        update_settings_batch(state, {data, project}) {
            const object_settings_batch = new Settings_Batch(data);
            Vue.set(project.settings_batch, object_settings_batch.id, object_settings_batch);
        },
        add_settings_batch(state, {data, project}) {
            const object_settings_batch = new Settings_Batch(data);
            Vue.set(project.settings_batch, object_settings_batch.id, object_settings_batch);
        },
        add_template_worker(state, {data, project}) {
            const object_template_worker = new Template_Worker(data);
            Vue.set(project.templates_worker, object_template_worker.id, object_template_worker);
        },
        remove_template_worker(state, {template_worker, project}) {
            Vue.delete(project.templates_worker, template_worker.id);
        },
        remove_settings_batch(state, {settings_batch, project}) {
            Vue.delete(project.settings_batch, settings_batch.id);
        },
	},
	actions: {
        async set_slug_project_current({state, commit, getters, rootGetters, dispatch}, slug_project_current) {
        	commit('set_slug_project_current', slug_project_current);


        	if(slug_project_current != undefined)
        	{
        		if(getters.get_project_current.settings_batch == null) {
        			dispatch('sync_settings_batch', getters.get_project_current);
        		}
        		if(getters.get_project_current.templates == null) {
        			dispatch('sync_templates_worker', getters.get_project_current);
        		}
        		console.log(`SET ${slug_project_current}`)
        		
        	}
        },
        async load_projects({state, commit, getters, rootGetters, dispatch}) {
            if(getters.get_object_projects == null) {

            	await dispatch('make_request', {
            		method: 'get',
            		url: rootGetters.get_url_api({
            			url: state.url_api_projects, 
            		}),
            	}, { root: true }).then(response => {
			    	// console.log(response.data)
                	commit('set_projects', response.data);
            	});

				// await axios.get(rootGetters.get_url_api(state.url_api_status_block, use_sandbox))
			 //    .then(response => {
    //             	commit('set_status_block', {'data_status_block': response.data, use_sandbox});
			 //    })
			}
        },
        async sync_settings_batch({state, commit, getters, rootGetters, dispatch}, project) {
        	await dispatch('make_request', {
        		method: 'get',
        		url: rootGetters.get_url_api({
        			url: state.url_api_projects_settings_batch, 
        			project: project,
        		}),
        	}, { root: true }).then(response => {
            	commit('set_settings_batch', {
            		data: response.data,
            		project: project,
            	});
        	});
        },
        async sync_templates_worker({state, commit, getters, rootGetters, dispatch}, project) {
        	await dispatch('make_request', {
        		method: 'get',
        		url: rootGetters.get_url_api({
        			url: state.url_api_projects_templates_worker, 
        			project: project,
        		}),
        	}, { root: true }).then(response => {
            	commit('set_templates_worker', {
            		data: response.data,
            		project: project,
            	});
        	});
        },
        async create_settings_batch({state, commit, getters, rootGetters, dispatch}, data) {
        	console.log(data);

			await dispatch('make_request', {
        		method: 'post',
        		url: rootGetters.get_url_api({
        			url: state.url_api_projects_settings_batch, 
        			project: data.project,
        		}),
    			data: data.settings_batch,
        	}, { root: true }).then(response => {
            	commit('add_settings_batch', {
            		data: response.data,
            		project: data.project,
            	});
        	});
        },
        async create_template_worker({state, commit, getters, rootGetters, dispatch}, data) {
            await dispatch('make_request', {
                method: 'post',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_worker, 
                    project: data.project,
                }),
                data: data.template_worker,
            }, { root: true }).then(response => {
                console.log(response);
                commit('add_template_worker', {
                    data: response.data,
                    project: data.project,
                });
            });
        },
        async delete_settings_batch({state, commit, getters, rootGetters, dispatch}, data) {
            await dispatch('make_request', {
                method: 'delete',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_settings_batch, 
                    project: data.project,
                    value: data.settings_batch.id
                }),
            }, { root: true }).then(response => {
                data.callback();
                commit('remove_settings_batch', {
                    settings_batch: data.settings_batch,
                    project: data.project,
                });
            });
        },
        async delete_template_worker({state, commit, getters, rootGetters, dispatch}, data) {
            await dispatch('make_request', {
                method: 'delete',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_worker, 
                    project: data.project,
                    value: data.template_worker.id
                }),
            }, { root: true }).then(response => {
                data.callback();
                commit('remove_template_worker', {
                    template_worker: data.template_worker,
                    project: data.project,
                });
            });
        },
        async edit_settings_batch({state, commit, getters, rootState, rootGetters, dispatch}, {data}) {
			// const changes = project.get_changes(project_new);
			// changes['slug'] = project.slug;

            const data_changed = data.settings_batch_current.get_changes(data.settings_batch_new);
            console.log(data_changed)

            if(Object.keys(data_changed).length == 0) return;

            await dispatch('make_request', {
                method: 'put',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_settings_batch, 
                    project: data.project,
                    value: data.settings_batch_current.id
                }),
                data: data_changed
            }, { root: true }).then(response => {
                console.log(response);
                // data.callback();
                commit('update_settings_batch', {
                    data: response.data,
                    project: data.project,
                });
            });


			// await axios.put(
			// 	rootGetters.get_url_api(state.url_api_projects_settings_batch, false, project.slug),
			// 	JSON.stringify(project.get_changes(project_new)),
			// 	// project.get_changes_as_formdata(project_new),
			// 	{
			// 		headers: {
			// 			"X-CSRFToken": rootState.token_csrf,
			// 			// "Content-Type": 'multipart/form-data',
			// 			"Content-Type": 'application/json',
			// 		},
			// 	},
			// )
		 //    .then(response => {
   //          	commit('edit_project', response.data);
		 //    })
        },
        async validate_name({state, commit, getters, rootState, rootGetters, dispatch}, name) {
        	const response = await dispatch('make_request', {
        		method: 'get',
        		url: rootGetters.get_url_api(state.url_api_projects_check_uniqueness, false, name),
        	}, { root: true });
        	
        	return response
        },
        async create_project({state, commit, getters, rootState, rootGetters, dispatch}, name) {
        	const response = await dispatch('make_request', {
        		method: 'post',
        		url: rootGetters.get_url_api(state.url_api_projects, false),
        		data: {
        			name: name,
        		}
        	}, { root: true });
        	
        	return response
        },
	},
}