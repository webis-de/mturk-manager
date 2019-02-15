import { store } from '../store/vuex';
import { Service_Endpoint } from './service_endpoint';

class Class_Service_Templates {
  async load_all(
    project = store.getters['moduleProjects/get_project_current'],
  ) {
    await this.load('assignment', project);
    await this.load('hit', project);
    await this.load('global', project);
    await this.load('worker', project);
  }

  async load(
    type_template,
    project = store.getters['moduleProjects/get_project_current'],
  ) {
    const response_templates = await Service_Endpoint.make_request({
      method: 'get',
      url: {
        path: store.getters.get_url(
          `url_api_projects_templates_${type_template}`,
          'moduleProjects',
        ),
        project,
      },
    });

    store.commit(`moduleProjects/set_templates_${type_template}`, {
      data: response_templates.data,
      project,
    });
  }

  async create({ type_template, template, project }) {
    const response = await Service_Endpoint.make_request({
      method: 'post',
      url: {
        path: store.getters.get_url(
          `url_api_projects_templates_${type_template}`,
          'moduleProjects',
        ),
        project,
      },
      data: template,
    });

    store.commit(`moduleProjects/add_template_${type_template}`, {
      data: response.data,
      project,
    });
  }

  async edit({
    type_template, template_current, template_new, project,
  }) {
    const data_changed = template_current.get_changes(template_new);

    if (Object.keys(data_changed).length === 0) return;

    const response = await Service_Endpoint.make_request({
      method: 'put',
      url: {
        path: store.getters.get_url(
          `url_api_projects_templates_${type_template}`,
          'moduleProjects',
        ),
        project,
        value: template_current.id,
      },
      data: data_changed,
    });

    store.commit(`moduleProjects/update_template_${type_template}`, {
      data: response.data,
      project,
    });
  }

  async delete({
    type_template, template, project, callback,
  }) {
    await Service_Endpoint.make_request({
      method: 'delete',
      url: {
        path: store.getters.get_url(
          `url_api_projects_templates_${type_template}`,
          'moduleProjects',
        ),
        project,
        value: template.id,
      },
    });

    callback();
    store.commit(`moduleProjects/remove_template_${type_template}`, {
      template,
      project,
    });
  }
}

export const Service_Templates = new Class_Service_Templates();
