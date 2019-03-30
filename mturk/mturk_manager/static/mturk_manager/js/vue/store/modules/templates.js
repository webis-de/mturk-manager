import _ from 'lodash';
import Vue from 'vue';
import {initPagination, setPagination} from '../../helpers';
import Template_Worker from '../../classes/template_worker';
import Template_Assignment from '../../classes/template_assignment';
import Template_HIT from '../../classes/template_hit';
import Template_Global from '../../classes/template_global';
import baseModule from './base.module';

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

    arrayItemsWorker: null,
    arrayItemsAssignment: null,
    arrayItemsHIT: null,
    arrayItemsGlobal: null,

    arrayItemsWorkerAll: null,
    arrayItemsAssignmentAll: null,
    arrayItemsHITAll: null,
    arrayItemsGlobalAll: null,

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
        value: 'height_frame',
        classes: ['text-xs-right'],
      },
      {
        text: '#Variables',
        value: 'count_parameters',
        sortable: false,
        classes: ['text-xs-right'],
      },
      {
        text: 'Assignment Template',
        value: 'template_assignment',
      },
      {
        text: 'Assignment HIT',
        value: 'template_hit',
      },
      {
        text: 'Assignment Global',
        value: 'template_global',
      },
      {
        text: 'Actions',
        value: 'actions',
        sortable: false,
        width: '10%',
      },
    ],

    arrayColumns: [
      {
        text: 'Name',
        value: 'name',
        classes: ['text-xs-left', 'pl-3'],
      },
      {
        text: 'Actions',
        value: 'actions',
        sortable: false,
        width: '10%',
      },
    ],
  },
  getters: {
  },
  mutations: {
    setPaginationWorker(state, { pagination, setPageTo1 }) {
      setPagination({
        pagination,
        setPageTo1,
        namePagination: 'paginationWorker',
        nameLocalStorage: 'pagination_templates_worker',
        state,
      });
    },
    setPaginationAssignment(state, { pagination, setPageTo1 }) {
      setPagination({
        pagination,
        setPageTo1,
        namePagination: 'paginationAssignment',
        nameLocalStorage: 'pagination_templates_assignment',
        state,
      });
    },
    setPaginationHIT(state, { pagination, setPageTo1 }) {
      setPagination({
        pagination,
        setPageTo1,
        namePagination: 'paginationHIT',
        nameLocalStorage: 'pagination_templates_hit',
        state,
      });
    },
    setPaginationGlobal(state, { pagination, setPageTo1 }) {
      setPagination({
        pagination,
        setPageTo1,
        namePagination: 'paginationGlobal',
        nameLocalStorage: 'pagination_templates_global',
        state,
      });
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

      const templateNew = new classTemplate(data);

      Vue.set(
        state[nameState],
        _.findIndex(state[nameState], template => template.id === templateNew.id),
        templateNew,
      );
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
        _.findIndex(state[nameState], item => data.id === item.id),
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
  },
});
