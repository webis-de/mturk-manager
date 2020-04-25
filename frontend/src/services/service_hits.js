import { store } from '../store/vuex';
import { ServiceEndpoint } from './endpoint.service';
import { BaseLoadPageService } from './baseLoadPage.service';
import HIT from '../classes/hit';

class Class_Service_HITs extends BaseLoadPageService {
  async load_page(pagination, filters) {
    const useSandbox = store.state.module_app.use_sandbox;

    return Class_Service_HITs.loadPageInternal({
      pagination,
      filters,
      url: {
        path: store.getters.get_url(
          'url_api_projects_hits',
          'moduleHITs',
        ),
        use_sandbox: useSandbox,
        project: store.getters['moduleProjects/get_project_current'],
      },
      callback(response) {
        store.commit('moduleHITs/setState', {
          objectState: response.data.data.map((hit) => new HIT(hit)),
          nameState: useSandbox === true ? 'arrayHITsSandbox' : 'arrayHITs',
        });
      },
    });
  }

  async loadHIT(idHit) {
    const response = await ServiceEndpoint.makeRequest({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'url_api_projects_hits',
          'moduleHITs',
        ),
        project: store.getters['moduleProjects/get_project_current'],
        value: idHit,
      },
      params: {
        expand: '__batch__settings_batch__template_worker__',
      },
    });

    return new HIT(response.data);
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
