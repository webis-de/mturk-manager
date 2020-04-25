import _ from 'lodash';
import Vue from 'vue';
import { store } from '../store/vuex';
import { Service_Endpoint } from './service_endpoint';
import { Service_Batches } from './service_batches';
import { BaseLoadPageService } from './baseLoadPage.service';
import Worker from '../classes/workers';

class Class_Service_Workers extends BaseLoadPageService {
  async load_workers({ list_ids, use_sandbox, append }) {
    if (_.size(list_ids) === 0) {
      return;
    }

    const response = await Service_Endpoint.make_request({
      method: 'patch',
      url: {
        path: store.getters.get_url('url_api_workers', 'moduleWorkers'),
        use_sandbox,
        project: store.getters['moduleProjects/get_project_current'],
      },
      data: Array.from(list_ids),
    });

    const data_workers = response.data;

    if (append === true) {
      store.commit('moduleWorkers/append_workers', {
        data_workers,
        use_sandbox,
      });
    } else {
      store.commit('moduleWorkers/set_workers', {
        data_workers,
        use_sandbox,
      });
    }

    Service_Batches.add_workers({
      object_workers: store.getters['moduleWorkers/get_object_workers'](
        use_sandbox,
      ),
      use_sandbox,
    });

    const blocks_hard = await Service_Endpoint.make_request({
      method: 'patch',
      url: {
        path: store.getters.get_url(
          'url_api_workers_get_blocks_hard',
          'moduleWorkers',
        ),
        use_sandbox,
        project: store.getters['moduleProjects/get_project_current'],
      },
      data: Array.from(list_ids),
    });

    const array_blocks_hard = blocks_hard.data;
    store.commit('moduleWorkers/set_blocks_hard', {
      array_blocks_hard,
      use_sandbox,
    });
  }

  async update_status_block_soft({ worker, is_blocked }) {
    const use_sandbox = store.state.module_app.use_sandbox;
    const project = store.getters['moduleProjects/get_project_current'];

    const response = await Service_Endpoint.make_request({
      method: 'put',
      url: {
        path: store.getters.get_url('url_api_workers', 'moduleWorkers'),
        value: worker.id,
        use_sandbox,
        project,
      },
      data: {
        is_blocked_soft: is_blocked,
      },
    });

    store.commit('moduleWorkers/update_status_block_soft', {
      worker,
      data: response.data,
      use_sandbox,
    });
  }

  async update_status_block_hard({ worker, is_blocked }) {
    const use_sandbox = store.state.module_app.use_sandbox;
    const project = store.getters['moduleProjects/get_project_current'];

    const response = await Service_Endpoint.make_request({
      method: 'put',
      url: {
        path: store.getters.get_url('url_api_workers', 'moduleWorkers'),
        value: worker.id,
        use_sandbox,
        project,
      },
      data: {
        is_blocked_hard: is_blocked,
      },
    });

    store.commit('moduleWorkers/update_status_block_hard', {
      worker,
      data: response.data,
      use_sandbox,
    });
  }

  async update_status_block_global({ worker, is_blocked }) {
    const use_sandbox = store.state.module_app.use_sandbox;
    const project = store.getters['moduleProjects/get_project_current'];

    const response = await Service_Endpoint.make_request({
      method: 'put',
      url: {
        path: store.getters.get_url('url_api_workers', 'moduleWorkers'),
        value: worker.id,
        use_sandbox,
        project,
      },
      data: {
        is_blocked_global: is_blocked,
      },
    });

    store.commit('moduleWorkers/update_status_block_global', {
      worker,
      data: response.data,
      use_sandbox,
    });
  }

  async update_count_assignments_limit({ worker, value }) {
    const use_sandbox = store.state.module_app.use_sandbox;
    const project = store.getters['moduleProjects/get_project_current'];

    const response = await Service_Endpoint.make_request({
      method: 'put',
      url: {
        path: store.getters.get_url('url_api_workers', 'moduleWorkers'),
        value: worker.id,
        use_sandbox,
        project,
      },
      data: {
        count_assignments_limit: value,
      },
    });

    store.commit('moduleWorkers/set_worker', {
      worker,
      worker_new: response.data,
      array_fields: ['count_assignments_limit'],
    });
  }

  async loadPage(pagination, filters) {
    const useSandbox = store.state.module_app.use_sandbox;

    return Class_Service_Workers.loadPageInternal({
      pagination,
      filters,
      url: {
        path: store.getters.get_url(
          'url_api_workers',
          'moduleWorkers',
        ),
        use_sandbox: useSandbox,
        project: store.getters['moduleProjects/get_project_current'],
      },
      callback(response) {
        store.commit('moduleWorkers/setState', {
          objectState: response.data.data.map(worker => new Worker(worker)),
          nameState: useSandbox === true ? 'arrayWorkersSandbox' : 'arrayWorkers',
        });

        // fetch worker blocks asynchronously
        Service_Endpoint.make_request({
          method: 'patch',
          url: {
            path: store.getters.get_url(
              'url_api_workers_get_blocks_hard',
              'moduleWorkers',
            ),
            use_sandbox: useSandbox,
            project: store.getters['moduleProjects/get_project_current'],
          },
        }).then((data) => {
          store.commit('moduleWorkers/set_blocks_hard', {
            data: data.data,
            use_sandbox: useSandbox,
          });
        });
      },
    });
  }
}

export const Service_Workers = new Class_Service_Workers();
