import {Service_Endpoint} from "./service_endpoint";
import {store} from "../store/vuex";

class Class_Settings_Batch
{
    async load()
    {
        const project = store.getters['moduleProjects/get_project_current'];

        const response = await Service_Endpoint.make_request({
            method: 'get',
            url: {
                path: store.getters["get_url"]('url_api_projects_settings_batch', 'moduleProjects'),
                project
            },
        });

        store.commit('moduleProjects/set_settings_batch', {
            data: response.data,
            project,
        });
    }

    async create({settings_batch, project})
    {
        const response = await Service_Endpoint.make_request({
            method: 'post',
            url: {
                path: store.getters["get_url"]('url_api_projects_settings_batch', 'moduleProjects'),
                project
            },
            data: settings_batch,
        });

        store.commit('moduleProjects/add_settings_batch', {
            data: response.data,
            project: project,
        });
    }

    async edit({settings_batch_current, settings_batch_new, project})
    {
        const data_changed = settings_batch_current.get_changes(settings_batch_new);

        if(Object.keys(data_changed).length === 0) return;

        const response = await Service_Endpoint.make_request({
            method: 'put',
            url: {
                path: store.getters["get_url"]('url_api_projects_settings_batch', 'moduleProjects'),
                value: settings_batch_current.id,
                project
            },
            data: data_changed
        })

        store.commit('moduleProjects/update_settings_batch', {
            data: response.data,
            project: project,
        });
    }



    async delete({settings_batch, project, callback})
    {
        const response = await Service_Endpoint.make_request({
            method: 'delete',
            url: {
                path: store.getters["get_url"]('url_api_projects_settings_batch', 'moduleProjects'),
                project,
                value: settings_batch.id
            },
        });

        callback();
        store.commit('moduleProjects/remove_settings_batch', {
            settings_batch,
            project,
        });
    }
}

export const Service_Settings_Batch = new Class_Settings_Batch();
