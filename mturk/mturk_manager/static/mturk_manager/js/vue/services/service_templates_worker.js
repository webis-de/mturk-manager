import {store} from "../store/vuex";
import {Service_Endpoint} from "./service_endpoint";

class Class_Service_Templates_Worker {
    async load(project=store.getters['moduleProjects/get_project_current']) {
        const response_templates_worker = await Service_Endpoint.make_request({
            method: 'get',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_worker', 'moduleProjects'),
                project,
            },
        });

		store.commit('moduleProjects/set_templates_worker', {
		    data: response_templates_worker.data,
            project
        });
    }

    async create({template_worker, project}) {
        const response = await Service_Endpoint.make_request({
            method: 'post',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_worker', 'moduleProjects'),
                project
            },
            data: template_worker,
        });

        store.commit('moduleProjects/add_template_worker', {
            data: response.data,
            project: project,
        });
    }

    async edit({template_worker_current, template_worker_new, project})
    {
        const data_changed = template_worker_current.get_changes(template_worker_new);

        if(Object.keys(data_changed).length === 0) return;

        const response = await Service_Endpoint.make_request({
            method: 'put',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_worker', 'moduleProjects'),
                project,
                value: template_worker_current.id
            },
            data: data_changed
        })

        store.commit('moduleProjects/update_template_worker', {
            data: response.data,
            project: project,
        });
    }

    async delete({template_worker, project, callback}) {
        const response = await Service_Endpoint.make_request({
            method: 'delete',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_worker', 'moduleProjects'),
                project,
                value: template_worker.id
            },
        });

        callback();
        store.commit('moduleProjects/remove_template_worker', {
            template_worker: template_worker,
            project: project,
        });
    }
}

export const Service_Templates_Worker = new Class_Service_Templates_Worker();