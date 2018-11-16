import Vue from 'vue';
import axios from 'axios';
import _ from 'lodash';
import Project from '../../classes/project';
import Settings_Batch from '../../classes/settings_batch';
import Template_Worker from '../../classes/template_worker';
import Template_Assignment from '../../classes/template_assignment';
import Template_HIT from '../../classes/template_hit';
import Template_Global from '../../classes/template_global';
import { router } from '../..//index.js';

export const moduleProjects = {
	namespaced: true,
	state: {
		object_projects: null,
		slug_project_current: null,

        url_api_projects: undefined,
        url_api_projects_check_uniqueness: undefined,
        url_api_projects_settings_batch: undefined,
        url_api_projects_templates_worker: undefined,
        url_api_projects_templates_assignment: undefined,
        url_api_projects_clear_sandbox: undefined,
        url_api_ping: null,

        response_data_projects: undefined,
	},
	getters: {
		get_project_current(state) {
            if(state.slug_project_current == undefined) return {};
            console.log('state.sliiiiig', state.slug_project_current)
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
            state.url_api_projects_templates_assignment = config.url_api_projects_templates_assignment;
            state.url_api_projects_templates_hit = config.url_api_projects_templates_hit;
            state.url_api_projects_templates_global = config.url_api_projects_templates_global;
            state.url_api_projects_clear_sandbox = config.url_api_projects_clear_sandbox;
            state.url_api_ping = config.url_api_ping;
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

                if(object_template_worker.template_assignment != undefined)
                {
                    Vue.set(object_template_worker, 'template_assignment', project.templates_assignment[object_template_worker.template_assignment]);
                } 
                if(object_template_worker.template_hit != undefined)
                {
                    Vue.set(object_template_worker, 'template_hit', project.templates_hit[object_template_worker.template_hit]);
                } 
                if(object_template_worker.template_global != undefined)
                {
                    Vue.set(object_template_worker, 'template_global', project.templates_global[object_template_worker.template_global]);
                } 
            });
        },
        set_templates_assignment(state, {data, project}) {
            project.templates_assignment = {};

            _.forEach(data, function(data_templates_assignment) {
                const object_template_assignment = new Template_Assignment(data_templates_assignment);
                Vue.set(project.templates_assignment, object_template_assignment.id, object_template_assignment);
            });
        },
        set_templates_hit(state, {data, project}) {
            project.templates_hit = {};

            _.forEach(data, function(data_templates_hit) {
                const object_template_hit = new Template_HIT(data_templates_hit);
                Vue.set(project.templates_hit, object_template_hit.id, object_template_hit);
            });
        },
        set_templates_global(state, {data, project}) {
            project.templates_global = {};
            _.forEach(data, function(data_templates_global) {
                const object_template_global = new Template_Global(data_templates_global);
                Vue.set(project.templates_global, object_template_global.id, object_template_global);
            });
        },
        set_response_data_projects(state, data_projects) {
            state.response_data_projects = data_projects;
        },
        add_to_response_data_projects(state, data_project) {
            state.response_data_projects.push(data_project);
        },
        set_projects(state, data_projects) {
            state.object_projects= {};
            
            _.forEach(data_projects, function(data_project){
                const object_project = new Project(data_project);
                Vue.set(state.object_projects, object_project.slug, object_project);
            });
        },
        add_project(state, data_project) {
            console.log('added project');
            const object_project = new Project(data_project);
            Vue.set(state.object_projects, object_project.slug, object_project);
            console.log(state.object_projects[data_project.slug]);

        },
        set_project(state, {project, project_new, array_fields}) {
            _.forEach(array_fields, function(name_field) {
                Vue.set(project, name_field, project_new[name_field]);
            });   
        },
        update_settings_batch(state, {data, project}) {
            const object_settings_batch = new Settings_Batch(data);
            Vue.set(project.settings_batch, object_settings_batch.id, object_settings_batch);
        },
        update_template_worker(state, {data, project}) {
            const template_worker = new Template_Worker(data);
            Vue.set(project.templates_worker, template_worker.id, template_worker);

            if(template_worker.template_assignment != undefined)
            {
                Vue.set(template_worker, 'template_assignment', project.templates_assignment[template_worker.template_assignment]);
            } 

            if(template_worker.template_hit != undefined)
            {
                Vue.set(template_worker, 'template_hit', project.templates_hit[template_worker.template_hit]);
            } 

            if(template_worker.template_global != undefined)
            {
                Vue.set(template_worker, 'template_global', project.templates_global[template_worker.template_global]);
            } 
        },
        update_template_assignment(state, {data, project}) {
            // const template_assignment = new Template_Assignment(data);
            // Vue.set(project.templates_assignment, template_assignment.id, template_assignment);
            project.templates_assignment[data.id].update(data);
        },
        update_template_hit(state, {data, project}) {
            // const template_hit = new Template_HIT(data);
            // Vue.set(project.templates_hit, template_hit.id, template_hit);
            project.templates_hit[data.id].update(data);
        },
        update_template_global(state, {data, project}) {
            project.templates_global[data.id].update(data);
            // const template_global = new Template_Global(data);
            // Vue.set(project.templates_global, template_global.id, template_global);
        },
        add_settings_batch(state, {data, project}) {
            const object_settings_batch = new Settings_Batch(data);
            Vue.set(project.settings_batch, object_settings_batch.id, object_settings_batch);
        },
        add_template_worker(state, {data, project}) {
            const object_template_worker = new Template_Worker(data);
            Vue.set(project.templates_worker, object_template_worker.id, object_template_worker);
            if(object_template_worker.template_assignment != undefined)
            {
                Vue.set(object_template_worker, 'template_assignment', project.templates_assignment[object_template_worker.template_assignment]);
            } 
        },
        add_template_assignment(state, {data, project}) {
            const object_template_assignment = new Template_Assignment(data);
            Vue.set(project.templates_assignment, object_template_assignment.id, object_template_assignment);
        },
        add_template_hit(state, {data, project}) {
            const object_template_hit = new Template_HIT(data);
            Vue.set(project.templates_hit, object_template_hit.id, object_template_hit);
        },
        add_template_global(state, {data, project}) {
            const object_template_global = new Template_Global(data);
            Vue.set(project.templates_global, object_template_global.id, object_template_global);
        },
        remove_template_worker(state, {template_worker, project}) {
            Vue.delete(project.templates_worker, template_worker.id);
        },
        remove_template_assignment(state, {template_assignment, project}) {
            Vue.delete(project.templates_assignment, template_assignment.id);
        },
        remove_template_hit(state, {template_hit, project}) {
            Vue.delete(project.templates_hit, template_hit.id);
        },
        remove_template_global(state, {template_global, project}) {
            Vue.delete(project.templates_global, template_global.id);
        },
        remove_settings_batch(state, {settings_batch, project}) {
            Vue.delete(project.settings_batch, settings_batch.id);
        },
        set_ping(state, {project, data}) {
            Vue.set(project, 'datetime_visited', new Date(data.datetime));
        },
        delete_project(state, { project }) {
            Vue.delete(state.object_projects, project.slug);
        },
	},
	actions: {
        async set_slug_project_current({state, commit, getters, rootGetters, dispatch}, slug_project_current) {
            const project_has_changed = state.slug_project_current != slug_project_current ? true : false;

        	commit('set_slug_project_current', slug_project_current);

            if(project_has_changed == true) 
            {
                // reset database
    			await dispatch('reset_projects');

                // load initial values for project
                if(slug_project_current != undefined)
                {
                    if(getters.get_project_current.settings_batch == null) {
                        await dispatch('sync_settings_batch', getters.get_project_current);
            		}
                    if(getters.get_project_current.templates_assignment == null) {
                        dispatch('sync_templates_assignment', getters.get_project_current).then(() => {
                            if(getters.get_project_current.templates_hit == null) {
                                dispatch('sync_templates_hit', getters.get_project_current).then(() => {
                                    if(getters.get_project_current.templates_global == null) {
                                        dispatch('sync_templates_global', getters.get_project_current).then(() => {
                                            if(getters.get_project_current.templates_worker == null) {
                                                dispatch('sync_templates_worker', getters.get_project_current);
                                            }
                                        });
                                    }
                                });
                            }
                        });
                    }
                    
            		// console.log(`SET ${slug_project_current}`)
            		
            	}
            }

        },
        async load_projects({state, commit, getters, rootGetters, dispatch}) {
            if(getters.get_object_projects == null) {

            	const response = await dispatch('make_request', {
            		method: 'get',
            		url: rootGetters.get_url_api({
            			url: state.url_api_projects, 
            		}),
            	}, { root: true })

                console.log(response)
                if(response.success == true)
                {
                    commit('set_response_data_projects', response.data);
                	commit('set_projects', response.data);
                } else {
                    // console.log(router)
                    // router.push({name: 'error'}); 
                }


				// await axios.get(rootGetters.get_url_api(state.url_api_status_block, use_sandbox))
			 //    .then(response => {
    //             	commit('set_status_block', {'data_status_block': response.data, use_sandbox});
			 //    })
			}
        },
        async reset_projects({state, commit, getters, rootGetters, dispatch}) {
            commit('set_projects', state.response_data_projects);
            commit('moduleBatches/reset', null, { root: true });
            commit('moduleHITs/reset', null, { root: true });
            commit('moduleAssignments/reset', null, { root: true });
            commit('moduleWorkers/reset', null, { root: true });
        },
        async sync_settings_batch({state, commit, getters, rootGetters, dispatch}, project) {
        	await dispatch('make_request', {
        		method: 'get',
        		url: rootGetters.get_url_api({
        			url: state.url_api_projects_settings_batch, 
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
                }),
            }, { root: true }).then(response => {
                commit('set_templates_worker', {
                    data: response.data,
                    project: project,
                });
            });
        },
        async sync_templates_assignment({state, commit, getters, rootGetters, dispatch}, project) {
            await dispatch('make_request', {
                method: 'get',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_assignment, 
                }),
            }, { root: true }).then(response => {
                commit('set_templates_assignment', {
                    data: response.data,
                    project: project,
                });
            });
        },
        async sync_templates_hit({state, commit, getters, rootGetters, dispatch}, project) {
            await dispatch('make_request', {
                method: 'get',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_hit, 
                }),
            }, { root: true }).then(response => {
                commit('set_templates_hit', {
                    data: response.data,
                    project: project,
                });
            });
        },
        async sync_templates_global({state, commit, getters, rootGetters, dispatch}, project) {
            await dispatch('make_request', {
                method: 'get',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_global, 
                }),
            }, { root: true }).then(response => {
                commit('set_templates_global', {
                    data: response.data,
                    project: project,
                });
            });
        },
        async create_settings_batch({state, commit, getters, rootGetters, dispatch}, data) {
			await dispatch('make_request', {
        		method: 'post',
        		url: rootGetters.get_url_api({
        			url: state.url_api_projects_settings_batch, 
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
        async create_template_assignment({state, commit, getters, rootGetters, dispatch}, data) {
            await dispatch('make_request', {
                method: 'post',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_assignment, 
                }),
                data: data.template_assignment,
            }, { root: true }).then(response => {
                console.log(response);
                commit('add_template_assignment', {
                    data: response.data,
                    project: data.project,
                });
            });
        },
        async create_template_hit({state, commit, getters, rootGetters, dispatch}, data) {
            await dispatch('make_request', {
                method: 'post',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_hit, 
                }),
                data: data.template_hit,
            }, { root: true }).then(response => {
                console.log(response);
                commit('add_template_hit', {
                    data: response.data,
                    project: data.project,
                });
            });
        },
        async create_template_global({state, commit, getters, rootGetters, dispatch}, data) {
            await dispatch('make_request', {
                method: 'post',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_global, 
                }),
                data: data.template_global,
            }, { root: true }).then(response => {
                console.log(response);
                commit('add_template_global', {
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
        async delete_template_assignment({state, commit, getters, rootGetters, dispatch}, data) {
            await dispatch('make_request', {
                method: 'delete',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_assignment, 
                    value: data.template_assignment.id
                }),
            }, { root: true }).then(response => {
                data.callback();
                commit('remove_template_assignment', {
                    template_assignment: data.template_assignment,
                    project: data.project,
                });
            });
        },
        async delete_template_hit({state, commit, getters, rootGetters, dispatch}, data) {
            await dispatch('make_request', {
                method: 'delete',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_hit, 
                    value: data.template_hit.id
                }),
            }, { root: true }).then(response => {
                data.callback();
                commit('remove_template_hit', {
                    template_hit: data.template_hit,
                    project: data.project,
                });
            });
        },
        async delete_template_global({state, commit, getters, rootGetters, dispatch}, data) {
            await dispatch('make_request', {
                method: 'delete',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_global, 
                    value: data.template_global.id
                }),
            }, { root: true }).then(response => {
                data.callback();
                commit('remove_template_global', {
                    template_global: data.template_global,
                    project: data.project,
                });
            });
        },
        async set_count_assignments_max_per_worker({state, commit, getters, rootState, rootGetters, dispatch}, {project, count_assignments_max_per_worker}) {
            await dispatch('make_request', {
                method: 'put',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects, 
                    value: project.slug,
                }),
                data: {
                    count_assignments_max_per_worker
                }
            }, { root: true }).then(response => {
                commit('set_project', {
                    project,
                    project_new: response.data,
                    array_fields: ['count_assignments_max_per_worker'],
                });
            });
        },
        async set_message_reject_default({state, commit, getters, rootState, rootGetters, dispatch}, {project, message_reject}) {
            await dispatch('make_request', {
                method: 'put',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects, 
                    value: project.slug,
                }),
                data: {
                    message_reject
                }
            }, { root: true }).then(response => {
                commit('set_project', {
                    project,
                    project_new: response.data,
                    array_fields: ['message_reject_default'],
                });

                commit('moduleMessagesReject/add_message_reject', {
                    message_reject: response.data.message_reject_default
                }, { root: true });
            });
        },
        async edit_settings_batch({state, commit, getters, rootState, rootGetters, dispatch}, {data}) {
            const data_changed = data.settings_batch_current.get_changes(data.settings_batch_new);

            if(Object.keys(data_changed).length == 0) return;

            await dispatch('make_request', {
                method: 'put',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_settings_batch, 
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
        },
        async edit_template_worker({state, commit, getters, rootState, rootGetters, dispatch}, {data}) {
            const data_changed = data.template_worker_current.get_changes(data.template_worker_new);

            if(Object.keys(data_changed).length == 0) return;

            await dispatch('make_request', {
                method: 'put',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_worker, 
                    value: data.template_worker_current.id
                }),
                data: data_changed
            }, { root: true }).then(response => {
                commit('update_template_worker', {
                    data: response.data,
                    project: data.project,
                });
            });
        },
        async edit_template_assignment({state, commit, getters, rootState, rootGetters, dispatch}, {data}) {
            const data_changed = data.template_assignment_current.get_changes(data.template_assignment_new);

            if(Object.keys(data_changed).length == 0) return;

            await dispatch('make_request', {
                method: 'put',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_assignment, 
                    value: data.template_assignment_current.id
                }),
                data: data_changed
            }, { root: true }).then(response => {
                commit('update_template_assignment', {
                    data: response.data,
                    project: data.project,
                });
            });
        },
        async edit_template_hit({state, commit, getters, rootState, rootGetters, dispatch}, {data}) {
            const data_changed = data.template_hit_current.get_changes(data.template_hit_new);

            if(Object.keys(data_changed).length == 0) return;

            await dispatch('make_request', {
                method: 'put',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_hit, 
                    value: data.template_hit_current.id
                }),
                data: data_changed
            }, { root: true }).then(response => {
                commit('update_template_hit', {
                    data: response.data,
                    project: data.project,
                });
            });
        },
        async edit_template_global({state, commit, getters, rootState, rootGetters, dispatch}, {data}) {
            const data_changed = data.template_global_current.get_changes(data.template_global_new);

            if(Object.keys(data_changed).length == 0) return;

            await dispatch('make_request', {
                method: 'put',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_templates_global, 
                    value: data.template_global_current.id
                }),
                data: data_changed
            }, { root: true }).then(response => {
                commit('update_template_global', {
                    data: response.data,
                    project: data.project,
                });
            });
        },
        async validate_name({state, commit, getters, rootState, rootGetters, dispatch}, name) {
        	const response = await dispatch('make_request', {
        		method: 'get',
        		url: rootGetters.get_url_api({
        			url: state.url_api_projects_check_uniqueness, 
        			value: name,
        		}),
        	}, { root: true });
        	
        	return response
        },
        async create_project({state, commit, getters, rootState, rootGetters, dispatch}, name) {
        	const response = await dispatch('make_request', {
        		method: 'post',
        		url: rootGetters.get_url_api({
        			url: state.url_api_projects,
        		}),
        		data: {
        			name: name,
        		}
        	}, { root: true });

            commit('add_project', response.data);
            commit('add_to_response_data_projects', response.data);
            return response.data.slug;
        },
        async clear_sandbox({state, commit, rootGetters, dispatch}) {
            const response = await dispatch('make_request', {
                method: 'delete',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_clear_sandbox,
                }),
            }, { root: true });

            commit('moduleBatches/clear_sandbox', null, {root: true});
            commit('moduleHITs/clear_sandbox', null, {root: true});
            commit('moduleAssignments/clear_sandbox', null, {root: true});
            commit('moduleWorkers/clear_sandbox', null, {root: true});
        },
        async ping({commit, state, rootGetters, dispatch}) {
            const project_current = rootGetters['moduleProjects/get_project_current'];
            const slug_project_current = project_current.slug;
            if(slug_project_current == null) return;

            const response = await dispatch('make_request', {
                method: 'put',
                url: rootGetters.get_url_api({
                    url: state.url_api_ping,
                }),
            }, { root: true });
            // console.log(response);
            commit('set_ping', {
                project: project_current,
                data: response.data,
            });
        },
        async delete_project({commit, state, rootGetters, dispatch}, router) {
            const project = rootGetters['moduleProjects/get_project_current'];

            const response = await dispatch('make_request', {
                method: 'delete',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects,
                    value: project.slug,
                }),
            }, { root: true });

            router.push({name: 'dashboard'}); 

            commit('delete_project', {
                project,
            });
        },
	},
}