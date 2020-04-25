import Vue from 'vue';
import _ from 'lodash';
import { parse } from 'date-fns';
import Project from '../../classes/project';
import SettingsBatch from '../../classes/settings_batch';
import Template_Worker from '../../classes/template_worker';
import Template_Assignment from '../../classes/template_assignment';
import Template_HIT from '../../classes/template_hit';
import Template_Global from '../../classes/template_global';
import baseModule from './base.module';

export const moduleProjects = _.merge({}, baseModule, {
  namespaced: true,
  state: {
    projectCurrent: null,
    object_projects: null,
    slug_project_current: null,

    url_api_projects: undefined,
    url_api_projects_check_uniqueness: undefined,
    url_api_projects_clear_sandbox: undefined,
    url_api_ping: null,
    urlApiTasks: null,

    arrayTasks: [],

    // response_data_projects: undefined,
  },
  getters: {
    getProjectCurrent(state) {
      if (
        state.slug_project_current === null
        || state.slug_project_current === undefined
        || state.object_projects === null
      ) {
        return {};
      }

      return state.object_projects[state.slug_project_current];
    },
    get_project_current(state) {
      if (
        state.slug_project_current === null
        || state.slug_project_current === undefined
        || state.object_projects === null
      ) {
        return {};
      }

      return state.object_projects[state.slug_project_current];
    },
    //  	get_object_project: (state, getters, rootState) => {
    //  		console.log(rootState.name_project)
    // return state.object_projects;
    //  	},
    get_object_projects: (state) => state.object_projects,
    get_slug_project_current(state) {
      return state.slug_project_current;
    },
  },
  mutations: {
    edit_project(state, data) {
      const project = new Project(data);
      Vue.set(state.object_projects, project.slug, project);
    },
    set_slug_project_current(state, slug_project_current) {
      state.slug_project_current = slug_project_current;

      // if (
      //   state.slug_project_current === null
      //   || state.slug_project_current === undefined
      //   || state.object_projects === null
      // ) {
      //
      // }
      // state.projectCurrent = ;
    },
    set_urls(state, config) {
      state.url_api_projects = config.url_api_projects;
      state.url_api_projects_check_uniqueness = config.url_api_projects_check_uniqueness;
      state.url_api_projects_clear_sandbox = config.url_api_projects_clear_sandbox;
      state.url_api_ping = config.url_api_ping;
      state.urlApiTasks = config.url_api_projects_tasks;
    },
    set_settings_batch(state, { data, project }) {
      project.settings_batch = {};

      _.forEach(data, (data_settings_batch) => {
        const object_settings_batch = new SettingsBatch(data_settings_batch);
        Vue.set(
          project.settings_batch,
          object_settings_batch.id,
          object_settings_batch,
        );
      });
    },
    set_templates_worker(state, { data, project }) {
      project.templates_worker = {};

      _.forEach(data, (data_templates_worker) => {
        const object_template_worker = new Template_Worker(
          data_templates_worker,
        );
        Vue.set(
          project.templates_worker,
          object_template_worker.id,
          object_template_worker,
        );

        if (object_template_worker.template_assignment != undefined) {
          Vue.set(
            object_template_worker,
            'template_assignment',
            project.templates_assignment[
              object_template_worker.template_assignment
            ],
          );
        }
        if (object_template_worker.template_hit != undefined) {
          Vue.set(
            object_template_worker,
            'template_hit',
            project.templates_hit[object_template_worker.template_hit],
          );
        }
        if (object_template_worker.template_global != undefined) {
          Vue.set(
            object_template_worker,
            'template_global',
            project.templates_global[object_template_worker.template_global],
          );
        }
      });
    },
    set_templates_assignment(state, { data, project }) {
      project.templates_assignment = {};
      _.forEach(data, (data_templates_assignment) => {
        const object_template_assignment = new Template_Assignment(
          data_templates_assignment,
        );
        Vue.set(
          project.templates_assignment,
          object_template_assignment.id,
          object_template_assignment,
        );
      });
    },
    set_templates_hit(state, { data, project }) {
      project.templates_hit = {};

      _.forEach(data, (data_templates_hit) => {
        const object_template_hit = new Template_HIT(data_templates_hit);
        Vue.set(
          project.templates_hit,
          object_template_hit.id,
          object_template_hit,
        );
      });
    },
    set_templates_global(state, { data, project }) {
      project.templates_global = {};
      _.forEach(data, (data_templates_global) => {
        const object_template_global = new Template_Global(
          data_templates_global,
        );
        Vue.set(
          project.templates_global,
          object_template_global.id,
          object_template_global,
        );
      });
    },
    // set_response_data_projects(state, data_projects) {
    //     state.response_data_projects = data_projects;
    // },
    // add_to_response_data_projects(state, data_project) {
    //     state.response_data_projects.push(data_project);
    // },
    // remove_from_response_data_projects(state, data_project) {
    //     const index = _.findIndex(state.response_data_projects, (p) => p.id === data_project.id);
    //     Vue.delete(state.response_data_projects, index);
    // },
    set_projects(state, data_projects) {
      state.object_projects = {};

      _.forEach(data_projects, (data_project) => {
        const object_project = new Project(data_project);
        Vue.set(state.object_projects, object_project.slug, object_project);
      });
    },
    add_project(state, project) {
      Vue.set(state.object_projects, project.slug, project);
    },
    set_project(state, { project, project_new, array_fields }) {
      _.forEach(array_fields, (name_field) => {
        Vue.set(project, name_field, project_new[name_field]);
      });
    },
    // update_template_worker(state, { data, project }) {
    //   const template_worker = new Template_Worker(data);
    //   Vue.set(project.templates_worker, template_worker.id, template_worker);
    //
    //   if (template_worker.template_assignment != undefined) {
    //     Vue.set(
    //       template_worker,
    //       'template_assignment',
    //       project.templates_assignment[template_worker.template_assignment],
    //     );
    //   }
    //
    //   if (template_worker.template_hit != undefined) {
    //     Vue.set(
    //       template_worker,
    //       'template_hit',
    //       project.templates_hit[template_worker.template_hit],
    //     );
    //   }
    //
    //   if (template_worker.template_global != undefined) {
    //     Vue.set(
    //       template_worker,
    //       'template_global',
    //       project.templates_global[template_worker.template_global],
    //     );
    //   }
    // },
    // update_template_assignment(state, { data, project }) {
    //   // const template_assignment = new Template_Assignment(data);
    //   // Vue.set(project.templates_assignment, template_assignment.id, template_assignment);
    //   project.templates_assignment[data.id].update(data);
    // },
    // update_template_hit(state, { data, project }) {
    //   // const template_hit = new Template_HIT(data);
    //   // Vue.set(project.templates_hit, template_hit.id, template_hit);
    //   project.templates_hit[data.id].update(data);
    // },
    // update_template_global(state, { data, project }) {
    //   project.templates_global[data.id].update(data);
    //   // const template_global = new Template_Global(data);
    //   // Vue.set(project.templates_global, template_global.id, template_global);
    // },
    add_template_worker(state, { data, project }) {
      const object_template_worker = new Template_Worker(data);
      Vue.set(
        project.templates_worker,
        object_template_worker.id,
        object_template_worker,
      );
      if (object_template_worker.template_assignment != undefined) {
        Vue.set(
          object_template_worker,
          'template_assignment',
          project.templates_assignment[
            object_template_worker.template_assignment
          ],
        );
      }
    },
    add_template_assignment(state, { data, project }) {
      const object_template_assignment = new Template_Assignment(data);
      Vue.set(
        project.templates_assignment,
        object_template_assignment.id,
        object_template_assignment,
      );
    },
    add_template_hit(state, { data, project }) {
      const object_template_hit = new Template_HIT(data);
      Vue.set(
        project.templates_hit,
        object_template_hit.id,
        object_template_hit,
      );
    },
    add_template_global(state, { data, project }) {
      const object_template_global = new Template_Global(data);
      Vue.set(
        project.templates_global,
        object_template_global.id,
        object_template_global,
      );
    },
    remove_template_worker(state, { template, project }) {
      Vue.delete(project.templates_worker, template.id);
    },
    remove_template_assignment(state, { template, project }) {
      Vue.delete(project.templates_assignment, template.id);
    },
    remove_template_hit(state, { template, project }) {
      Vue.delete(project.templates_hit, template.id);
    },
    remove_template_global(state, { template, project }) {
      Vue.delete(project.templates_global, template.id);
    },
    set_ping(state, { project, data }) {
      Vue.set(project, 'datetime_visited', parse(data.datetime));
    },
    delete_project(state, { project }) {
      Vue.delete(state.object_projects, project.slug);
    },
    reset: (state) => {
      state.arrayTasks = [];
    },
  },
  actions: {
    reset_projects({
      commit,
    }) {
      commit('reset');
      commit('moduleBatches/reset', null, { root: true });
      commit('moduleHITs/reset', null, { root: true });
      commit('moduleAssignments/reset', null, { root: true });
      commit('moduleWorkers/reset', null, { root: true });
    },
    clear_sandbox({
      state, commit, rootGetters, dispatch,
    }) {
      commit('moduleBatches/clear_sandbox', null, { root: true });
      commit('moduleHITs/clear_sandbox', null, { root: true });
      commit('moduleAssignments/clear_sandbox', null, { root: true });
      commit('moduleWorkers/clear_sandbox', null, { root: true });
    },
  },
});
