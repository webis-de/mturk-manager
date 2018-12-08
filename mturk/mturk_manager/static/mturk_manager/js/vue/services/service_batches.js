import {Service_Endpoint} from "./service_endpoint";
import {store} from "../store/vuex";
import {Service_HITs} from "./service_hits";

class Class_Service_Batches {
	// async load_batches(force=false)
    // {
	// 	const use_sandbox = store.getters["get_use_sandbox"];
    //
	// 	if(store.getters['moduleBatches/get_object_batches'](use_sandbox) == null || force) {
    //         const response = await Service_Endpoint.make_request({
    //             method: 'get',
    //             url: {
    //                 url: store.getters["get_url"]('url_api_projects_batches', 'moduleBatches'),
    //                 use_sandbox,
    //                 project: store.getters['moduleProjects/get_project_current'],
    //             },
    //         });
    //
    //         const data_batches = response.data;
    //
    //         store.commit('moduleBatches/set_batches', {
    //             data_batches,
    //             use_sandbox
    //         });
    //
    //         await Service_HITs.set_hits({
    //             object_batches: store.getters['moduleBatches/get_object_batches'](use_sandbox),
    //             data_batches,
    //             use_sandbox
    //         });
    //     }
    // }

    async create(data)
    {
		const use_sandbox = store.getters["get_use_sandbox"];
		const project = store.getters['moduleProjects/get_project_current'];

        const response = await Service_Endpoint.make_request({
            method: 'post',
            url: {
                url: store.getters["get_url"]('url_api_projects_batches', 'moduleBatches'),
                use_sandbox,
                project,
            },
            data: data,
        });

        store.commit('moduleBatches/add_batch', {
            data_batch: response.data,
            use_sandbox,
        });

        store.commit('moduleHITs/set_hits', {
            'object_batches': store.getters['moduleBatches/get_object_batches'](use_sandbox),
            'data_batches': [response.data],
            use_sandbox
        });
    }

    // async sync_mturk() {
	// 	const use_sandbox = store.getters["get_use_sandbox"];
	// 	const project = store.getters['moduleProjects/get_project_current'];
    //
    //     store.commit('moduleBatches/set_is_syncing_mturk', true);
    //     const response = await Service_Endpoint.make_request({
    //         method: 'patch',
    //         url: {
    //             url: store.getters["get_url"]('url_api_projects_batches', 'moduleBatches'),
    //             project,
    //             use_sandbox,
    //         },
    //      });
    //
    //     const data_batches = response.data;
    //
    //     await Service_HITs.append_hits({
    //         data_batches,
    //         use_sandbox
    //
    //     });
    //
    //     store.commit('moduleBatches/set_is_syncing_mturk', false);
    // }

    // add_workers({object_workers, use_sandbox})
    // {
    //     store.commit('moduleBatches/add_workers', {
    //         object_workers,
    //         use_sandbox,
    //     });
    // }


    async load_page(pagination) {
		const use_sandbox = store.getters["get_use_sandbox"];

        const response = await Service_Endpoint.make_request({
            method: 'get',
            url: {
                url: store.getters["get_url"]('url_api_projects_batches', 'moduleBatches'),
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

        store.commit('moduleBatches/set_batches', {
            data: response.data.data,
            use_sandbox
        });

        return response.data.items_total;
    }

    get_batch(id_batch) {
        console.log('id_batch', id_batch);
    }
}


export const Service_Batches = new Class_Service_Batches();