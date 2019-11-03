import { store } from '../store/vuex';
import { Service_Endpoint } from './service_endpoint';
import { BaseLoadPageService } from './baseLoadPage.service';

class Class_Service_Templates extends BaseLoadPageService {
  constructor() {
    super();
    this.isLoadingWorkerAll = false;
    this.isLoadingAssignmentAll = false;
    this.isLoadingHITAll = false;
    this.isLoadingGlobalAll = false;
  }

  async loadPageWorker(pagination, filters, nameState) {
    return Class_Service_Templates.loadPage(pagination, filters, 'worker', nameState);
  }

  async loadPageAssignment(pagination, filters) {
    return Class_Service_Templates.loadPage(pagination, filters, 'assignment');
  }

  async loadPageHIT(pagination, filters) {
    return Class_Service_Templates.loadPage(pagination, filters, 'hit');
  }

  async loadPageGlobal(pagination, filters) {
    return Class_Service_Templates.loadPage(pagination, filters, 'global');
  }

  static async loadPage(pagination, filters, typeTemplate, nameState) {
    const project = store.getters['moduleProjects/get_project_current'];

    let urlTemplate;
    switch (typeTemplate) {
      case 'worker':
        urlTemplate = 'urlApiProjectsTemplatesWorker';
        break;
      case 'assignment':
        urlTemplate = 'urlApiProjectsTemplatesAssignment';
        break;
      case 'hit':
        urlTemplate = 'urlApiProjectsTemplatesHIT';
        break;
      case 'global':
        urlTemplate = 'urlApiProjectsTemplatesGlobal';
        break;
      default:
        break;
    }

    return super.loadPageInternal({
      pagination,
      filters,
      url: {
        path: store.getters.get_url(
          urlTemplate,
          'moduleTemplates',
        ),
        project,
      },
      callback(response) {
        if (nameState !== undefined) {
          store.commit('moduleTemplates/setState', {
            objectState: response.data.data,
            nameState,
          });
        } else {
          store.commit('moduleTemplates/setItems', {
            data: response.data.data,
            typeTemplate,
          });
        }
      },
    });
  }

  async getAll({ typeTemplate, force = true }) {
    let nameState;
    let urlTemplate;
    let nameLoading;

    switch (typeTemplate) {
      case 'workerAll':
        nameState = 'arrayItemsWorkerAll';
        urlTemplate = 'urlApiProjectsTemplatesWorkerAll';
        nameLoading = 'isLoadingWorkerAll';
        break;
      case 'assignmentAll':
        nameState = 'arrayItemsAssignmentAll';
        urlTemplate = 'urlApiProjectsTemplatesAssignmentAll';
        nameLoading = 'isLoadingAssignmentAll';
        break;
      case 'hitAll':
        nameState = 'arrayItemsHITAll';
        urlTemplate = 'urlApiProjectsTemplatesHITAll';
        nameLoading = 'isLoadingHITAll';
        break;
      case 'globalAll':
        nameState = 'arrayItemsGlobalAll';
        urlTemplate = 'urlApiProjectsTemplatesGlobalAll';
        nameLoading = 'isLoadingGlobalAll';
        break;
      default:
        break;
    }

    const arrayItems = store.state.moduleTemplates[nameState];

    if (arrayItems !== null && force === false) {
      return;
    }

    if (this[nameLoading] === true) {
      return;
    }

    this[nameLoading] = true;

    const project = store.getters['moduleProjects/get_project_current'];

    const response = await Service_Endpoint.make_request({
      method: 'get',
      url: {
        path: store.getters.get_url(
          urlTemplate,
          'moduleTemplates',
        ),
        project,
      },
      params: {
        fields: [
          'id',
          'name',
        ],
      },
    });

    store.commit('moduleTemplates/setItems', {
      data: response.data,
      typeTemplate,
    });

    this[nameLoading] = false;
  }

  // async load_all(
  //   project = store.getters['moduleProjects/get_project_current'],
  // ) {
  //   await this.load('assignment', project);
  //   await this.load('hit', project);
  //   await this.load('global', project);
  //   // await this.load('worker', project);
  // }

  // async load(
  //   typeTemplate,
  //   project = store.getters['moduleProjects/get_project_current'],
  // ) {
  //   const response = await Service_Endpoint.make_request({
  //     method: 'get',
  //     url: {
  //       path: store.getters.get_url(
  //         `url_api_projects_templates_${typeTemplate}`,
  //         'moduleProjects',
  //       ),
  //       project,
  //     },
  //   });
  //
  //   store.commit(`moduleProjects/set_templates_${typeTemplate}`, {
  //     data: response.data,
  //     project,
  //   });
  // }

  async create({ typeTemplate, template, project }) {
    let urlTemplate;
    switch (typeTemplate) {
      case 'worker':
        urlTemplate = 'urlApiProjectsTemplatesWorker';
        break;
      case 'assignment':
        urlTemplate = 'urlApiProjectsTemplatesAssignment';
        break;
      case 'hit':
        urlTemplate = 'urlApiProjectsTemplatesHIT';
        break;
      case 'global':
        urlTemplate = 'urlApiProjectsTemplatesGlobal';
        break;
      default:
        break;
    }

    const response = await Service_Endpoint.make_request({
      method: 'post',
      url: {
        path: store.getters.get_url(
          urlTemplate,
          'moduleTemplates',
        ),
        project,
      },
      data: template,
    });

    store.commit(`moduleTemplates/add`, {
      data: response.data,
      typeTemplate,
    });

    return response.data;
  }

  async edit({
    typeTemplate, templateCurrent, templateNew, project,
  }) {
    let urlTemplate;
    switch (typeTemplate) {
      case 'worker':
        urlTemplate = 'urlApiProjectsTemplatesWorker';
        break;
      case 'assignment':
        urlTemplate = 'urlApiProjectsTemplatesAssignment';
        break;
      case 'hit':
        urlTemplate = 'urlApiProjectsTemplatesHIT';
        break;
      case 'global':
        urlTemplate = 'urlApiProjectsTemplatesGlobal';
        break;
      default:
        break;
    }


    const dataChanged = templateCurrent.get_changes(templateNew);

    if (Object.keys(dataChanged).length === 0) return;

    const response = await Service_Endpoint.make_request({
      method: 'put',
      url: {
        path: store.getters.get_url(
          urlTemplate,
          'moduleTemplates',
        ),
        project,
        value: templateCurrent.id,
      },
      data: dataChanged,
    });

    store.commit('moduleTemplates/update', {
      data: response.data,
      typeTemplate,
    });
  }

  async delete({
    typeTemplate, template, project, callback,
  }) {
    let urlTemplate;
    switch (typeTemplate) {
      case 'worker':
        urlTemplate = 'urlApiProjectsTemplatesWorker';
        break;
      case 'assignment':
        urlTemplate = 'urlApiProjectsTemplatesAssignment';
        break;
      case 'hit':
        urlTemplate = 'urlApiProjectsTemplatesHIT';
        break;
      case 'global':
        urlTemplate = 'urlApiProjectsTemplatesGlobal';
        break;
      default:
        break;
    }

    await Service_Endpoint.make_request({
      method: 'delete',
      url: {
        path: store.getters.get_url(
          urlTemplate,
          'moduleTemplates',
        ),
        project,
        value: template.id,
      },
    });

    callback();

    store.commit('moduleTemplates/delete', {
      data: template,
      typeTemplate,
    });

    return template;
  }

  cleanup({ typeTemplate, nameEvent, component, template, closeDialog = true }) {
    component.$emit(nameEvent);

    if (closeDialog === true) {
      component.dialog = false;
    }

    if (nameEvent === 'created') {
      component.reset();
      store.commit('moduleTemplates/setItems', {
        data: [template],
        typeTemplate,
        add: true,
      });
    } else if(nameEvent === 'edited') {
      store.commit('moduleTemplates/update', {
        data: template,
        typeTemplate,
      });
    } else if(nameEvent === 'deleted') {
      store.commit('moduleTemplates/delete', {
        data: template,
        typeTemplate,
      });
    }
  }
}

export const Service_Templates = new Class_Service_Templates();
