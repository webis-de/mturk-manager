import { store } from '../store/vuex';
import { Service_Endpoint } from './service_endpoint';
import { getChanges } from '../helpers';
import Assignment from '../classes/assignment';
import { BaseLoadPageService } from './baseLoadPage.service';
import HIT from '../classes/hit';

class Class_Service_Assignments extends BaseLoadPageService {
  async set_assignments({ object_hits, data_batches, use_sandbox }) {
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

  async append_assignments({ data_batches, object_hits, use_sandbox }) {
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
    const useSandbox = store.state.module_app.use_sandbox;

    return Class_Service_Assignments.loadPageInternal({
      pagination,
      filters,
      url: {
        path: store.getters.get_url(
          'url_api_projects_assignments',
          'moduleAssignments',
        ),
        use_sandbox: useSandbox,
        project: store.getters['moduleProjects/get_project_current'],
      },
      callback(response) {
        store.commit('moduleAssignments/setState', {
          objectState: response.data.data.map(hit => new Assignment(hit)),
          nameState: useSandbox === true ? 'arrayAssignmentsSandbox' : 'arrayAssignments',
        });
      },
    });
  }

  async edit({ assignmentNew, assignmentCurrent }) {
    const dataChanged = getChanges(assignmentNew, assignmentCurrent);

    if (Object.keys(dataChanged).length === 0) return;

    const project = store.getters['moduleProjects/get_project_current'];

    const response = await Service_Endpoint.make_request({
      method: 'put',
      url: {
        path: store.getters.get_url(
          'url_api_projects_assignments',
          'moduleAssignments',
        ),
        project,
        value: assignmentCurrent.id,
      },
      data: dataChanged,
    });

    store.commit('moduleAssignments/update', {
      assignment: new Assignment(response.data),
    });
    // store.commit('moduleTemplates/update', {
    //   data: response.data,
    //   typeTemplate,
    // });
  }
}

export const Service_Assignments = new Class_Service_Assignments();
