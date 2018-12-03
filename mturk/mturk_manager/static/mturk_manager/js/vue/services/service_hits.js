import {store} from "../store/vuex";
import {Service_Assignments} from "./service_assignments";
import {Service_Endpoint} from "./service_endpoint";

class Class_Service_HITs {
    async load_page(pagination) {
		const use_sandbox = store.getters["get_use_sandbox"];

        const response = await Service_Endpoint.make_request({
            method: 'get',
            url: {
                url: store.getters["get_url"]('url_api_projects_hits', 'moduleHITs'),
                use_sandbox,
                project: store.getters['moduleProjects/get_project_current'],
            },
            params: {
                page: pagination.page,
                page_size: pagination.rowsPerPage,
                sort_by: pagination.sortBy,
                descending: pagination.descending,
            }
        });

        store.commit('moduleHITs/set_hits', {
            data: response.data.data,
            use_sandbox
        });

        return response.data.items_total;
    }
    // async set_hits({object_batches, data_batches, use_sandbox})
    // {
    //     store.commit('moduleHITs/set_hits', {
    //         object_batches,
    //         data_batches,
    //         use_sandbox
    //     });
    //
    //     await Service_Assignments.set_assignments({
    //         object_hits: store.getters['moduleHITs/get_object_hits'](use_sandbox),
    //         data_batches,
    //         use_sandbox
    //     });
    // }
    //
    // async append_hits({data_batches, use_sandbox})
    // {
    //      await Service_Assignments.append_assignments({
    //         data_batches,
    //         object_hits: store.getters['moduleHITs/get_object_hits'](use_sandbox),
    //         use_sandbox,
    //     });
    // }
}

export const Service_HITs = new Class_Service_HITs();