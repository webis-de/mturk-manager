import { store } from '../store/vuex';
import { Service_Endpoint } from './service_endpoint';

class ClassServiceFinances {
  async load({filters, typeItem}) {
    const use_sandbox = store.state.module_app.use_sandbox;

    const response = await Service_Endpoint.make_request({
      url: {
        path: store.getters.get_url(
          'url_api_projects_finances',
          'module_finances',
        ),
        use_sandbox,
        project: store.getters['moduleProjects/get_project_current'],
      },
      method: 'get',
      params: {
        typeItem,
        ...filters,
      },
    });

    return response.data;

    // store.commit('module_finances/setState', {
    //   objectState: response.data.sum_costs_max,
    //   nameState: 'sum_costs_max',
    // });
    //
    // store.commit('module_finances/setState', {
    //   objectState: response.data.sum_costs_so_far,
    //   nameState: 'sum_costs_so_far',
    // });
    //
    // store.commit('module_finances/setState', {
    //   objectState: response.data.sum_costs_pending,
    //   nameState: 'sum_costs_pending',
    // });
  }

  async load_balance() {
    const use_sandbox = store.state.module_app.use_sandbox;

    const response = await Service_Endpoint.make_request({
      url: {
        path: store.getters.get_url(
          'url_api_projects_balance',
          'module_finances',
        ),
        use_sandbox,
        project: store.getters['moduleProjects/get_project_current'],
      },
      method: 'get',
    });

    if (use_sandbox === true) {
      store.commit(
        'module_finances/set_balance_sandbox',
        response.data.balance,
      );
    } else {
      store.commit('module_finances/set_balance', response.data.balance);
    }
  }
}

export const ServiceFinances = new ClassServiceFinances();