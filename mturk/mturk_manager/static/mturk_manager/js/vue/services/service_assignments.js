import {store} from "../store/vuex";
import {Service_Workers} from "./service_worker";
import {Service_Endpoint} from "./service_endpoint";

class Class_Service_Assignments {
    async set_assignments({object_hits, data_batches, use_sandbox})
    {
        store.commit('moduleAssignments/set_assignments', {
            data_batches,
            object_hits,
            use_sandbox,
        });

        // await Service_Workers.load_workers({
        //     list_ids: store.getters['moduleAssignments/set_ids_worker'],
        //     use_sandbox,
        // });
    }

    async append_assignments({data_batches, object_hits, use_sandbox})
    {
        store.commit('moduleAssignments/set_assignments', {
            data_batches,
            object_hits,
            use_sandbox,
        });

        // await Service_Workers.load_workers({
        //     list_ids: store.getters['moduleAssignments/set_ids_worker'],
        //     use_sandbox,
        //     append: true,
        // });
    }

    async load_page(pagination, filters) {
		const use_sandbox = store.getters["get_use_sandbox"];
        const response = await Service_Endpoint.make_request({
            method: 'get',
            url: {
                url: store.getters["get_url"]('url_api_projects_assignments', 'moduleAssignments'),
                use_sandbox,
                project: store.getters['moduleProjects/get_project_current'],
            },
            params: {
                page: pagination.page,
                page_size: pagination.rowsPerPage,
                sort_by: pagination.sortBy,
                descending: pagination.descending,
                ...filters,
            }
        });

        store.commit('moduleAssignments/set_assignments', {
            data: response.data.data,
            use_sandbox
        });

        return response.data.items_total;
    }
}

export const Service_Assignments = new Class_Service_Assignments();