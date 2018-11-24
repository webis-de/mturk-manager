import {store} from "../store/vuex";
import {Service_Endpoint} from "./service_endpoint";

class Class_Service_Templates_Global {
    async load(project=store.getters['moduleProjects/get_project_current']) {
        const response_templates_global = await Service_Endpoint.make_request({
            method: 'get',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_global', 'moduleProjects'),
                project,
            },
        });

		store.commit('moduleProjects/set_templates_global', {
		    data: response_templates_global.data,
            project
        });
    }

    async create({template_global, project}) {
        const response = await Service_Endpoint.make_request({
            method: 'post',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_global', 'moduleProjects'),
                project
            },
            data: template_global,
        });

        store.commit('moduleProjects/add_template_global', {
            data: response.data,
            project: project,
        });
    }

    async edit({template_global_current, template_global_new, project})
    {
        const data_changed = template_global_current.get_changes(template_global_new);

        if(Object.keys(data_changed).length === 0) return;

        const response = await Service_Endpoint.make_request({
            method: 'put',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_global', 'moduleProjects'),
                project,
                value: template_global_current.id
            },
            data: data_changed
        })

        store.commit('moduleProjects/update_template_global', {
            data: response.data,
            project: project,
        });
    }

    async delete({template_global, project, callback}) {
        const response = await Service_Endpoint.make_request({
            method: 'delete',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_global', 'moduleProjects'),
                project,
                value: template_global.id
            },
        });

        callback();
        store.commit('moduleProjects/remove_template_global', {
            template_global: template_global,
            project: project,
        });
    }
}

export const Service_Templates_Global = new Class_Service_Templates_Global();