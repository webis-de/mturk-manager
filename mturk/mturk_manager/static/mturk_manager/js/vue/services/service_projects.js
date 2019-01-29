import Project from "../classes/project";
import {store} from '../store/vuex';
import {Service_Endpoint} from "./service_endpoint";
import {Service_Settings_Batch} from "./service_settings_batch";
import {Service_Templates} from "./service_templates";

class Class_Service_Projects {
	constructor()
	{
		this.id_interval = undefined;
	}

	async load_projects()
	{
		const use_sandbox = store.state['module_app']["use_sandbox"];

		if(store.getters['moduleProjects/get_object_projects'] == null) {
            const response = await Service_Endpoint.make_request({
                method: 'get',
                url: {
                    path: store.getters["get_url"]('url_api_projects', 'moduleProjects'),
                },
            });

            if (response.success === true) {
                // store.commit('moduleProjects/set_response_data_projects', response.data);
                store.commit('moduleProjects/set_projects', response.data);
                return true;
            } else {
                // console.log(router)
                // router.push({name: 'error'});
                return false;
            }
        }
	}

	async create_project(name)
	{
		const use_sandbox = store.state['module_app']["use_sandbox"];
		const response = await Service_Endpoint.make_request({
			method: 'post',
			url: {
				path: store.getters["get_url"]('url_api_projects', 'moduleProjects'),
			},
			data: {
				name: name,
			}
		});
		const project = new Project(response.data);

		store.commit('moduleProjects/add_project', project);
		// store.commit('moduleProjects/add_to_response_data_projects', response.data);

		return project;
	}

	async validate_name(name)
	{
        return await Service_Endpoint.make_request({
            method: 'get',
            url: {
                path: store.getters["get_url"]('url_api_projects_check_uniqueness', 'moduleProjects'),
                value: name,
            },
        });
	}

    set_slug_current(slug_project_new) {
        store.commit('moduleProjects/set_slug_project_current', slug_project_new);
    }

    load_project_data() {
	    const project = store.getters['moduleProjects/get_project_current'];

		// reset database
		store.dispatch('moduleProjects/reset_projects');

		clearInterval(this.id_interval);

		// load initial values for project
		if(project.slug !== undefined)
		{
			this.load_data(project);
			Service_Settings_Batch.load();
			Service_Templates.load_all();

                this.ping();
                this.id_interval = setInterval(() => {
                    this.ping();
                }, 1000 * 60 * 5);
		}
    }

    async clear_sandbox()
	{
		await Service_Endpoint.make_request({
			method: 'delete',
			url: {
                path: store.getters["get_url"]('url_api_projects_clear_sandbox', 'moduleProjects'),
				project: store.getters['moduleProjects/get_project_current'],
			},
		});

		store.dispatch('moduleProjects/clear_sandbox');
	}

	async delete({router})
	{
		const project = store.getters['moduleProjects/get_project_current'];

		const response = await Service_Endpoint.make_request({
			method: 'delete',
			url: {
				path: store.getters["get_url"]('url_api_projects', 'moduleProjects'),
				project,
				value: project.slug,
			},
		});

		// store.commit('moduleProjects/remove_from_response_data_projects', project);
		router.push({name: 'dashboard'});

		store.commit('moduleProjects/delete_project', {
			project,
		});
	}

	async set_message_reject_default({project, message_reject})
	{
		const response = await Service_Endpoint.make_request({
			method: 'put',
			url: {
				path: store.getters["get_url"]('url_api_projects', 'moduleProjects'),
				project,
				value: project.slug,
			},
			data: {
				message_reject
			}
		});

		store.commit('moduleProjects/set_project', {
			project,
			project_new: response.data,
			array_fields: ['message_reject_default'],
		});

		store.commit('moduleMessagesReject/add_message_reject', {
			message_reject: response.data.message_reject_default
		});
	}

	async set_count_assignments_max_per_worker({project, count_assignments_max_per_worker})
	{
		const response = await Service_Endpoint.make_request({
			method: 'put',
			url: {
				path: store.getters["get_url"]('url_api_projects', 'moduleProjects'),
				project,
				value: project.slug,
			},
			data: {
				count_assignments_max_per_worker
			}
		});

		store.commit('moduleProjects/set_project', {
			project,
			project_new: response.data,
			array_fields: ['count_assignments_max_per_worker'],
		});
	}


	async ping() {
		const project = store.getters['moduleProjects/get_project_current'];

		const slug_project_current = project.slug;
		if(slug_project_current == null) return;

		const response = await Service_Endpoint.make_request({
			method: 'put',
			url: {
				path: store.getters["get_url"]('url_api_ping', 'moduleProjects'),
				project,
			},
		});

		store.commit('moduleProjects/set_ping', {
			project,
			data: response.data,
		});
	}

    async load_data(project) {
		const response = await Service_Endpoint.make_request({
			method: 'get',
			url: {
				path: store.getters["get_url"]('url_api_projects', 'moduleProjects'),
				project,
				value: project.slug,
			},
		});

		project.sum_costs_max_sandbox = response.data.sum_costs_max_sandbox;
		project.max_costs_max_sandbox = response.data.max_costs_max_sandbox;
		project.min_costs_max_sandbox = response.data.min_costs_max_sandbox;

		project.sum_costs_so_far_sandbox = response.data.sum_costs_so_far_sandbox;
		project.max_costs_so_far_sandbox = response.data.max_costs_so_far_sandbox;
		project.min_costs_so_far_sandbox = response.data.min_costs_so_far_sandbox;

		project.sum_costs_max = response.data.sum_costs_max;
		project.max_costs_max = response.data.max_costs_max;
		project.min_costs_max = response.data.min_costs_max;

		project.sum_costs_so_far = response.data.sum_costs_so_far;
		project.max_costs_so_far = response.data.max_costs_so_far;
		project.min_costs_so_far = response.data.min_costs_so_far;


		// console.log('response', response.data);
		// store.commit('moduleProjects/set_ping', {
		// 	project,
		// 	data: response.data,
		// });
    }
}

export const Service_Projects = new Class_Service_Projects();
