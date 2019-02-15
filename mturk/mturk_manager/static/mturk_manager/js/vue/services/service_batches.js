import { Service_Endpoint } from './service_endpoint';
import { store } from '../store/vuex';
import Batch from '../classes/batch';

class Class_Service_Batches {
  // async load_batches(force=false)
  // {
  // 	const use_sandbox = store.state.module_app.use_sandbox;
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

  async create(data) {
    const use_sandbox = store.state.module_app.use_sandbox;
    const project = store.getters['moduleProjects/get_project_current'];

    const response = await Service_Endpoint.make_request({
      method: 'post',
      url: {
        path: store.getters.get_url(
          'url_api_projects_batches',
          'moduleBatches',
        ),
        use_sandbox,
        project,
      },
      data,
    });

    // store.commit('moduleBatches/add_batch', {
    //     data_batch: response.data,
    //     use_sandbox,
    // });

    // store.commit('moduleHITs/set_hits', {
    //     'object_batches': store.getters['moduleBatches/get_object_batches'](use_sandbox),
    //     'data_batches': [response.data],
    //     use_sandbox
    // });
  }

  async sync_mturk() {
    const use_sandbox = store.state.module_app.use_sandbox;
    const project = store.getters['moduleProjects/get_project_current'];

    store.commit('moduleBatches/set_is_syncing_mturk', true);
    const response = await Service_Endpoint.make_request({
      method: 'patch',
      url: {
        path: store.getters.get_url(
          'url_api_projects_batches',
          'moduleBatches',
        ),
        project,
        use_sandbox,
      },
    });

    const data_batches = response.data;

    // await Service_HITs.append_hits({
    //     data_batches,
    //     use_sandbox
    //
    // });

    store.commit('moduleBatches/set_is_syncing_mturk', false);
  }

  // add_workers({object_workers, use_sandbox})
  // {
  //     store.commit('moduleBatches/add_workers', {
  //         object_workers,
  //         use_sandbox,
  //     });
  // }

  async load_page(pagination) {
    const use_sandbox = store.state.module_app.use_sandbox;

    const response = await Service_Endpoint.make_request({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'url_api_projects_batches',
          'moduleBatches',
        ),
        use_sandbox,
        project: store.getters['moduleProjects/get_project_current'],
      },
      params: {
        page: pagination.page,
        page_size: pagination.rowsPerPage,
        sort_by: pagination.sortBy,
        descending: pagination.descending,
      },
    });

    store.commit('moduleBatches/set_batches', {
      data: response.data.data,
      use_sandbox,
    });

    return response.data.items_total;
  }

  async get_batch(id_batch) {
    const response = await Service_Endpoint.make_request({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'url_api_projects_batches',
          'moduleBatches',
        ),
        project: store.getters['moduleProjects/get_project_current'],
        value: id_batch,
      },
    });

    return new Batch(response.data);
  }

  async download(params) {
    const response = await Service_Endpoint.make_request({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'url_api_projects_batches_download',
          'moduleBatches',
        ),
        project: store.getters['moduleProjects/get_project_current'],
      },
      params,
      options: {
        responseType: 'blob',
      },
    });

    const a = window.document.createElement('a');
    a.href = window.URL.createObjectURL(response.data, { type: 'text/plain' });
    a.download = 'filename.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  async get_download_info(params) {
    const response = await Service_Endpoint.make_request({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'url_api_projects_batches_download_info',
          'moduleBatches',
        ),
        project: store.getters['moduleProjects/get_project_current'],
      },
      params,
    });
    console.log('response', response.data);
    return response;
  }
}

export const Service_Batches = new Class_Service_Batches();
