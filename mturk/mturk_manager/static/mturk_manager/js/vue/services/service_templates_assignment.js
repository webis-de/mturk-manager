import {store} from "../store/vuex";
import {Service_Endpoint} from "./service_endpoint";

class Class_Service_Templates_Assignment {
    async load(project=store.getters['moduleProjects/get_project_current']) {

        const response_templates_assignment = await Service_Endpoint.make_request({
            method: 'get',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_assignment', 'moduleProjects'),
                project,
            },
        });

		store.commit('moduleProjects/set_templates_assignment', {
		    data: response_templates_assignment.data,
            project
        });
    }

    async create({template_assignment, project}) {
        const response = await Service_Endpoint.make_request({
            method: 'post',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_assignment', 'moduleProjects'),
                project
            },
            data: template_assignment,
        });

        store.commit('moduleProjects/add_template_assignment', {
            data: response.data,
            project,
        });
    }

    async edit({template_assignment_current, template_assignment_new, project})
    {
        const data_changed = template_assignment_current.get_changes(template_assignment_new);

        if(Object.keys(data_changed).length === 0) return;

        const response = await Service_Endpoint.make_request({
            method: 'put',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_assignment', 'moduleProjects'),
                project,
                value: template_assignment_current.id
            },
            data: data_changed
        })

        store.commit('moduleProjects/update_template_assignment', {
            data: response.data,
            project: project,
        });
    }

    async delete({template_assignment, project, callback}) {
        const response = await Service_Endpoint.make_request({
            method: 'delete',
            url: {
                url: store.getters["get_url"]('url_api_projects_templates_assignment', 'moduleProjects'),
                project,
                value: template_assignment.id
            },
        });

        callback();
        store.commit('moduleProjects/remove_template_assignment', {
            template_assignment: template_assignment,
            project: project,
        });
    }
}

export const Service_Templates_Assignment = new Class_Service_Templates_Assignment();