import { compareDesc, parse } from 'date-fns';
import Project from '../classes/project';
import { store } from '../store/vuex';
import { ServiceEndpoint } from './endpoint.service';
import { ServiceSettingsBatch } from './service_settings_batch';
import { ServiceTemplates } from './service_templates';
// import {router} from "./service_router.js";

class ClassServiceProjects {
  constructor() {
    this.id_interval = undefined;
    this.idTimeoutPollStatus = null;
  }

  async load_projects() {
    const response = await ServiceEndpoint.makeRequest({
      method: 'get',
      url: {
        path: store.getters.get_url('url_api_projects', 'moduleProjects'),
      },
      params: {
        fields: [
          'name',
          'slug',
          'datetime_visited',
        ],
      },
    });

    if (response.success === true) {
      // store.commit('moduleProjects/set_response_data_projects', response.data);
      store.commit('moduleProjects/set_projects', response.data);
      return true;
    }

    return false;
  }

  async create_project(name) {
    const { use_sandbox } = store.state.module_app;
    const response = await ServiceEndpoint.makeRequest({
      method: 'post',
      url: {
        path: store.getters.get_url('url_api_projects', 'moduleProjects'),
      },
      data: {
        name,
      },
    });
    const project = new Project(response.data);

    store.commit('moduleProjects/add_project', project);
    // store.commit('moduleProjects/add_to_response_data_projects', response.data);

    return project;
  }

  async validate_name(name) {
    return await ServiceEndpoint.makeRequest({
      method: 'get',
      url: {
        path: store.getters.get_url(
          'url_api_projects_check_uniqueness',
          'moduleProjects',
        ),
        value: name,
      },
    });
  }

  set_slug_current(slug_project_new) {
    store.commit('moduleProjects/set_slug_project_current', slug_project_new);
  }

  load_project_data() {
    const project = store.getters['moduleProjects/get_project_current'];

    // reset database
    store.dispatch('moduleProjects/reset_projects');

    clearInterval(this.id_interval);

    if (this.idTimeoutPollStatus !== null) {
      clearTimeout(this.idTimeoutPollStatus);
      this.idTimeoutPollStatus = null;
    }

    // load initial values for project
    if (project.slug !== undefined) {
      this.load_data(project);
      // ServiceSettingsBatch.load();
      // ServiceTemplates.load_all();

      this.startPollTasks();

      this.ping();
      this.id_interval = setInterval(() => {
        this.ping();
      }, 1000 * 60 * 5);
    }
  }

  async clear_sandbox() {
    await ServiceEndpoint.makeRequest({
      method: 'delete',
      url: {
        path: store.getters.get_url(
          'url_api_projects_clear_sandbox',
          'moduleProjects',
        ),
        project: store.getters['moduleProjects/get_project_current'],
      },
    });

    store.dispatch('moduleProjects/clear_sandbox');
  }

  async delete({ router }) {
    const project = store.getters['moduleProjects/get_project_current'];

    const response = await ServiceEndpoint.makeRequest({
      method: 'delete',
      url: {
        path: store.getters.get_url('url_api_projects', 'moduleProjects'),
        project,
        value: project.slug,
      },
    });

    // store.commit('moduleProjects/remove_from_response_data_projects', project);
    router.push({ name: 'dashboard' });

    store.commit('moduleProjects/delete_project', {
      project,
    });
  }

  async setMessageRejectDefault({ message }) {
    const project = store.getters['moduleProjects/get_project_current'];

    const response = await ServiceEndpoint.makeRequest({
      method: 'put',
      url: {
        path: store.getters.get_url('url_api_projects', 'moduleProjects'),
        project,
        value: project.slug,
      },
      data: {
        message_reject_default: message,
      },
    });

    store.commit('moduleProjects/set_project', {
      project,
      project_new: response.data,
      array_fields: ['message_reject_default'],
    });

    // store.commit('moduleMessages/add_message_reject', {
    //   message_reject: response.data.message_reject_default,
    // });
  }

  async set_count_assignments_max_per_worker({
    project,
    count_assignments_max_per_worker,
  }) {
    const response = await ServiceEndpoint.makeRequest({
      method: 'put',
      url: {
        path: store.getters.get_url('url_api_projects', 'moduleProjects'),
        project,
        value: project.slug,
      },
      data: {
        count_assignments_max_per_worker,
      },
    });

    store.commit('moduleProjects/set_project', {
      project,
      project_new: response.data,
      array_fields: ['count_assignments_max_per_worker'],
    });
  }

  async setAmountBudgetProject({
    project,
    amountBudgetProject,
  }) {
    const response = await ServiceEndpoint.makeRequest({
      method: 'put',
      url: {
        path: store.getters.get_url('url_api_projects', 'moduleProjects'),
        project,
        value: project.slug,
      },
      data: {
        amount_budget_max: amountBudgetProject,
      },
    });

    store.commit('moduleProjects/set_project', {
      project,
      project_new: response.data,
      array_fields: ['amount_budget_max'],
    });
  }

  async ping() {
    const project = store.getters['moduleProjects/get_project_current'];

    const slug_project_current = project.slug;
    if (slug_project_current == null) return;

    const response = await ServiceEndpoint.makeRequest({
      method: 'put',
      url: {
        path: store.getters.get_url('url_api_ping', 'moduleProjects'),
        project,
      },
    });

    store.commit('moduleProjects/set_ping', {
      project,
      data: response.data,
    });
  }

  async load_data(project) {
    const response = await ServiceEndpoint.makeRequest({
      method: 'get',
      url: {
        path: store.getters.get_url('url_api_projects', 'moduleProjects'),
        project,
        value: project.slug,
      },
    });

    store.dispatch('moduleProjects/updateState', {
      objectStateCurrent: project,
      objectStateNew: response.data,
      fields: [
        'amount_budget_max',
        'count_assignments_max_per_worker',
        'message_reject_default',

        'sum_costs_max_sandbox',
        'max_costs_max_sandbox',
        'min_costs_max_sandbox',

        'sum_costs_so_far_sandbox',
        'max_costs_so_far_sandbox',
        'min_costs_so_far_sandbox',

        'sum_costs_max',
        'max_costs_max',
        'min_costs_max',

        'sum_costs_so_far',
        'max_costs_so_far',
        'min_costs_so_far',
      ],
    });

    // project.sum_costs_max_sandbox = response.data.sum_costs_max_sandbox;
    // project.max_costs_max_sandbox = response.data.max_costs_max_sandbox;
    // project.min_costs_max_sandbox = response.data.min_costs_max_sandbox;
    //
    // project.sum_costs_so_far_sandbox = response.data.sum_costs_so_far_sandbox;
    // project.max_costs_so_far_sandbox = response.data.max_costs_so_far_sandbox;
    // project.min_costs_so_far_sandbox = response.data.min_costs_so_far_sandbox;
    //
    // project.sum_costs_max = response.data.sum_costs_max;
    // project.max_costs_max = response.data.max_costs_max;
    // project.min_costs_max = response.data.min_costs_max;
    //
    // project.sum_costs_so_far = response.data.sum_costs_so_far;
    // project.max_costs_so_far = response.data.max_costs_so_far;
    // project.min_costs_so_far = response.data.min_costs_so_far;

    // console.log('response', response.data);
    // store.commit('moduleProjects/set_ping', {
    // 	project,
    // 	data: response.data,
    // });
  }

  async startPollTasks() {
    if (this.idTimeoutPollStatus !== null) return;

    this.pollTasks();
  }

  async pollTasks() {
    const response = await ServiceEndpoint.makeRequest({
      method: 'get',
      url: {
        path: store.getters.get_url('urlApiTasks', 'moduleProjects'),
        project: store.getters['moduleProjects/get_project_current'],
      },
    });

    const arrayTasksServer = response.data.data;
    const arrayTasks = [...response.data.data];
    console.log('arrayTasksServer', arrayTasksServer);
    const setTasksOld = new Set(store.state.moduleProjects.arrayTasks.map((task) => task.task));
    const setTasksNew = new Set(arrayTasks.map((task) => task.task));

    const setFinishedTasks = new Set([...setTasksOld].filter((idTask) => !setTasksNew.has(idTask)));

    if (setFinishedTasks.size > 0) {
      for (const idTask of setFinishedTasks) {
        const taskFinished = store.state.moduleProjects.arrayTasks.find((task) => task.task === idTask);
        taskFinished.status = 2;
        arrayTasks.push(taskFinished);
      }
    }

    for (const task of store.state.moduleProjects.arrayTasks) {
      // console.warn('task', task);
    }

    arrayTasks.sort((a, b) => compareDesc(parse(a.datetime_created), parse(b.datetime_created)));

    store.commit('moduleProjects/setState', {
      objectState: arrayTasks,
      nameState: 'arrayTasks',
    });


    if (arrayTasksServer.filter((task) => task.status !== 3).length === 0) {
      clearTimeout(this.idTimeoutPollStatus);
      this.idTimeoutPollStatus = null;
    } else {
      this.idTimeoutPollStatus = setTimeout(() => {
        this.pollTasks();
      }, 1000);
    }
  }

  async deleteTask({ task }) {
    if (task.status === 3) {
      await ServiceEndpoint.makeRequest({
        method: 'delete',
        url: {
          path: store.getters.get_url('urlApiTasks', 'moduleProjects'),
          project: store.getters['moduleProjects/get_project_current'],
          value: task.id,
        },
      });
    }

    store.commit('moduleProjects/setState', {
      objectState: store.state.moduleProjects.arrayTasks.filter((taskCurrent) => taskCurrent.id !== task.id),
      nameState: 'arrayTasks',
    });
  }
}

export const ServiceProjects = new ClassServiceProjects();
