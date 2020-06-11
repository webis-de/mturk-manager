import _ from 'lodash';
import Vue from 'vue';
import { TemplateWorker as Template_Worker } from '@/classes/template_worker';
import Template_Assignment from '@/classes/template_assignment';
import Template_HIT from '@/classes/template_hit';
import Template_Global from '@/classes/template_global';
import baseModule from '@/store/modules/base.module';
import { TemplateAssignment } from '@/modules/template/templateAssignment.model';
import { TemplateHIT } from '@/modules/template/templateHIT.model';
import { TemplateGlobal } from '@/modules/template/templateGlobal.model';
import { TemplateWorker } from '@/modules/template/templateWorker.model';
import { classesHeaders } from '../../helpers';
import {TemplateBase} from "@/modules/template/templateBase.model";

interface StoreTemplateState {
  templatesWorker: { [key: string]: TemplateWorker};
  templatesAssignment: { [key: string]: TemplateAssignment};
  templatesHIT: { [key: string]: TemplateHIT};
  templatesGlobal: { [key: string]: TemplateGlobal};
}

export const moduleTemplates = _.merge({}, baseModule, {
  namespaced: true,
  state: {
    urlApiProjectsTemplatesWorker: undefined,
    urlApiProjectsTemplatesAssignment: undefined,
    urlApiProjectsTemplatesHIT: undefined,
    urlApiProjectsTemplatesGlobal: undefined,

    urlApiProjectsTemplatesWorkerAll: undefined,
    urlApiProjectsTemplatesAssignmentAll: undefined,
    urlApiProjectsTemplatesHITAll: undefined,
    urlApiProjectsTemplatesGlobalAll: undefined,

    templatesWorker: null,
    templatesAssignment: null,
    templatesHIT: null,
    templatesGlobal: null,

    // arrayItemsWorkerAll: null,
    // arrayItemsAssignmentAll: null,
    // arrayItemsHITAll: null,
    // arrayItemsGlobalAll: null,

    paginationWorker: {
      rowsPerPage: 5,
      sortBy: 'name',
      descending: true,
    },
    paginationAssignment: {
      rowsPerPage: 5,
      sortBy: 'name',
      descending: true,
    },
    paginationHIT: {
      rowsPerPage: 5,
      sortBy: 'name',
      descending: true,
    },
    paginationGlobal: {
      rowsPerPage: 5,
      sortBy: 'name',
      descending: true,
    },

    arrayColumnsWorker: [
      {
        text: 'Name',
        value: 'name',
        classes: ['text-xs-left', 'pl-3'],
      },
      {
        text: 'Height',
        value: 'heightFrame',
        width: '1px',
        align: 'end',
        class: classesHeaders,
      },
      {
        text: '#Variables',
        value: 'countParameters',
        sortable: false,
        width: '1px',
        align: 'end',
        class: classesHeaders,
      },
      {
        text: 'Assignment Template',
        value: 'templateAssignment',
        width: '1px',
        align: 'end',
        class: classesHeaders,
      },
      {
        text: 'Assignment HIT',
        value: 'templateHIT',
        width: '1px',
        align: 'end',
        class: classesHeaders,
      },
      {
        text: 'Assignment Global',
        value: 'templateGlobal',
        width: '1px',
        align: 'end',
        class: classesHeaders,
      },
      {
        text: '',
        value: 'actions',
        sortable: false,
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
    ],

    objectColumnsSelectedInitialGeneral: {
      name: true,
      heightFrame: true,
      countParameters: true,
      templateAssignment: true,
      templateHIT: true,
      templateGlobal: true,
      actions: true,
    },

    arrayColumns: [
      {
        text: 'Name',
        value: 'name',
        classes: ['text-xs-left', 'pl-3'],
      },
      {
        text: 'Type',
        value: 'type',
        width: '1px',
        align: 'end',
        class: classesHeaders,
      },
      {
        text: '',
        value: 'actions',
        sortable: false,
        align: 'end',
        class: classesHeaders,
        width: '1px',
      },
    ],
    objectColumnsSelectedInitial: {
      name: true,
      type: true,
      actions: true,
    },
  },
  getters: {
    templatesWorker(state: StoreTemplateState): TemplateWorker[] | null {
      if (state.templatesWorker === null) return null;

      return Object.values(state.templatesWorker);
    },
    templatesRequester(state: StoreTemplateState): TemplateBase[] | null {
      if (state.templatesWorker === null) return null;

      return Object.values(state.templatesAssignment)
        .concat(Object.values(state.templatesHIT))
        .concat(Object.values(state.templatesGlobal));
    },
  },
  mutations: {
    setTemplatesWorker(state: StoreTemplateState, { templates }: {templates: { [key: string]: TemplateWorker}}) {
      state.templatesWorker = templates;
    },
    setTemplatesAssignment(state: StoreTemplateState, { templates }: {templates: { [key: string]: TemplateAssignment}}) {
      state.templatesAssignment = templates;
    },
    setTemplatesHIT(state: StoreTemplateState, { templates }: {templates: { [key: string]: TemplateHIT}}) {
      state.templatesHIT = templates;
    },
    setTemplatesGlobal(state: StoreTemplateState, { templates }: {templates: { [key: string]: TemplateGlobal}}) {
      state.templatesGlobal = templates;
    },

    setItems(state, { data, typeTemplate, add = false }) {
      let nameState;
      let classTemplate;
      switch (typeTemplate) {
        case 'worker':
          nameState = 'arrayItemsWorker';
          classTemplate = Template_Worker;
          break;
        case 'assignment':
          nameState = 'arrayItemsAssignment';
          classTemplate = Template_Assignment;
          break;
        case 'hit':
          nameState = 'arrayItemsHIT';
          classTemplate = Template_HIT;
          break;
        case 'global':
          nameState = 'arrayItemsGlobal';
          classTemplate = Template_Global;
          break;
        case 'workerAll':
          nameState = 'arrayItemsWorkerAll';
          classTemplate = Template_Worker;
          break;
        case 'assignmentAll':
          nameState = 'arrayItemsAssignmentAll';
          classTemplate = Template_Assignment;
          break;
        case 'hitAll':
          nameState = 'arrayItemsHITAll';
          classTemplate = Template_HIT;
          break;
        case 'globalAll':
          nameState = 'arrayItemsGlobalAll';
          classTemplate = Template_Global;
          break;
        default:
          break;
      }

      if (add === false) {
        state[nameState] = [];
      }

      _.forEach(data, (dataTemplate) => {
        const hit = new classTemplate(dataTemplate);
        Vue.set(state[nameState], state[nameState].length, hit);
      });
    },
    update(state, { data, typeTemplate }) {
      let nameState;
      let classTemplate;
      switch (typeTemplate) {
        case 'worker':
          nameState = 'templatesWorker';
          classTemplate = Template_Worker;
          break;
        case 'assignment':
          nameState = 'templatesAssignment';
          // nameState = 'arrayItemsAssignment';
          classTemplate = Template_Assignment;
          break;
        case 'hit':
          nameState = 'templatesHIT';
          classTemplate = Template_HIT;
          break;
        case 'global':
          nameState = 'templatesGlobal';
          classTemplate = Template_Global;
          break;
        case 'workerAll':
          nameState = 'arrayItemsWorkerAll';
          classTemplate = Template_Worker;
          break;
        case 'assignmentAll':
          nameState = 'arrayItemsAssignmentAll';
          classTemplate = Template_Assignment;
          break;
        case 'hitAll':
          nameState = 'arrayItemsHITAll';
          classTemplate = Template_HIT;
          break;
        case 'globalAll':
          nameState = 'arrayItemsGlobalAll';
          classTemplate = Template_Global;
          break;
        default:
          break;
      }
      const templateNew = new classTemplate(data);
      console.warn('state[nameState]', state[nameState]);
      console.warn('templateNew.id', templateNew.id);
      console.warn('templateNew', templateNew);
      // Vue.set(
      //   state[nameState],
      //   templateNew.id,
      //   templateNew,
      // );
      console.warn('123', 123);
    },
    add(state, { data, typeTemplate }) {
      let nameState;
      let classTemplate;
      switch (typeTemplate) {
        case 'worker':
          nameState = 'arrayItemsWorker';
          classTemplate = Template_Worker;
          break;
        case 'assignment':
          nameState = 'arrayItemsAssignment';
          classTemplate = Template_Assignment;
          break;
        case 'hit':
          nameState = 'arrayItemsHIT';
          classTemplate = Template_HIT;
          break;
        case 'global':
          nameState = 'arrayItemsGlobal';
          classTemplate = Template_Global;
          break;
        default:
          break;
      }

      const templateNew = new classTemplate(data);

      Vue.set(
        state[nameState],
        state[nameState].length,
        templateNew,
      );
    },
    delete(state, { data, typeTemplate }) {
      let nameState;
      switch (typeTemplate) {
        case 'worker':
          nameState = 'arrayItemsWorker';
          break;
        case 'assignment':
          nameState = 'arrayItemsAssignment';
          break;
        case 'hit':
          nameState = 'arrayItemsHIT';
          break;
        case 'global':
          nameState = 'arrayItemsGlobal';
          break;
        case 'workerAll':
          nameState = 'arrayItemsWorkerAll';
          break;
        case 'assignmentAll':
          nameState = 'arrayItemsAssignmentAll';
          break;
        case 'hitAll':
          nameState = 'arrayItemsHITAll';
          break;
        case 'globalAll':
          nameState = 'arrayItemsGlobalAll';
          break;
        default:
          break;
      }

      Vue.delete(
        state[nameState],
        _.findIndex(state[nameState], (item) => data.id === item.id),
      );
    },
    setUrls(state, config) {
      state.urlApiProjectsTemplatesWorker = config.url_api_projects_templates_worker;
      state.urlApiProjectsTemplatesAssignment = config.url_api_projects_templates_assignment;
      state.urlApiProjectsTemplatesHIT = config.url_api_projects_templates_hit;
      state.urlApiProjectsTemplatesGlobal = config.url_api_projects_templates_global;

      state.urlApiProjectsTemplatesWorkerAll = config.url_api_projects_templates_worker_all;
      state.urlApiProjectsTemplatesAssignmentAll = config.url_api_projects_templates_assignment_all;
      state.urlApiProjectsTemplatesHITAll = config.url_api_projects_templates_hit_all;
      state.urlApiProjectsTemplatesGlobalAll = config.url_api_projects_templates_global_all;
    },
  },
  actions: {
    async init({ dispatch }) {
      await Promise.all([
        /**
         * init pagination
         */
        dispatch('loadState', {
          nameLocalStorage: 'pagination_templates_worker',
          nameState: 'paginationWorker',
        }),
        dispatch('loadState', {
          nameLocalStorage: 'pagination_templates_assignment',
          nameState: 'paginationAssignment',
        }),
        dispatch('loadState', {
          nameLocalStorage: 'pagination_templates_hit',
          nameState: 'paginationHIT',
        }),
        dispatch('loadState', {
          nameLocalStorage: 'pagination_templates_global',
          nameState: 'paginationGlobal',
        }),
      ]);
    },
    setTemplatesWorker({ commit }, { templates }) {
      commit('setTemplatesWorker', {
        templates,
      });
    },
    setTemplatesAssignment({ commit }, { templates }) {
      commit('setTemplatesAssignment', {
        templates,
      });
    },
    setTemplatesHIT({ commit }, { templates }) {
      commit('setTemplatesHIT', {
        templates,
      });
    },
    setTemplatesGlobal({ commit }, { templates }) {
      commit('setTemplatesGlobal', {
        templates,
      });
    },
  },
});
