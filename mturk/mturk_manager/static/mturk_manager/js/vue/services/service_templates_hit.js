import {store} from "../store/vuex";
import {Service_Endpoint} from "./service_endpoint";

class Class_Service_Templates_HIT {
    async load(project=store.getters['moduleProjects/get_project_current']) {
        const response_templates_hit = await Service_Endpoint.make_request({
            method: 'get',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_hit', 'moduleProjects'),
                project,
            },
        });

		store.commit('moduleProjects/set_templates_hit', {
		    data: response_templates_hit.data,
            project
        });
    }

    async create({template_hit, project}) {
        const response = await Service_Endpoint.make_request({
            method: 'post',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_hit', 'moduleProjects'),
                project
            },
            data: template_hit,
        });

        store.commit('moduleProjects/add_template_hit', {
            data: response.data,
            project: project,
        });
    }

    async edit({template_hit_current, template_hit_new, project})
    {
        const data_changed = template_hit_current.get_changes(template_hit_new);

        if(Object.keys(data_changed).length === 0) return;

        const response = await Service_Endpoint.make_request({
            method: 'put',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_hit', 'moduleProjects'),
                project,
                value: template_hit_current.id
            },
            data: data_changed
        })

        store.commit('moduleProjects/update_template_hit', {
            data: response.data,
            project: project,
        });
    }

    async delete({template_hit, project, callback}) {
        const response = await Service_Endpoint.make_request({
            method: 'delete',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_hit', 'moduleProjects'),
                project,
                value: template_hit.id
            },
        });

        callback();
        store.commit('moduleProjects/remove_template_hit', {
            template_hit: template_hit,
            project: project,
        });
    }
}

export const Service_Templates_HIT = new Class_Service_Templates_HIT();