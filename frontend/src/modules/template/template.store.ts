import _ from 'lodash';
import Vue from 'vue';
import baseModule from '@/store/modules/base.module';
import { TemplateAssignment } from '@/modules/template/templateAssignment.model';
import { TemplateHIT } from '@/modules/template/templateHIT.model';
import { TemplateGlobal } from '@/modules/template/templateGlobal.model';
import { TemplateWorker } from '@/modules/template/templateWorker.model';
import { classesHeaders } from '@/helpers';
import { TemplateBase } from '@/modules/template/templateBase.model';

interface StoreTemplateState {
  templatesWorker: { [key: string]: TemplateWorker};
  templatesAssignment: { [key: string]: TemplateAssignment};
  templatesHIT: { [key: string]: TemplateHIT};
  templatesGlobal: { [key: string]: TemplateGlobal};
}

export const moduleTemplates = _.merge({}, baseModule, {
  namespaced: true,
  state: {
    templatesWorker: null,
    templatesAssignment: null,
    templatesHIT: null,
    templatesGlobal: null,

    paginationWorker: {
      rowsPerPage: 5,
      sortBy: 'name',
      descending: true,
    },
    paginationRequester: {
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
    /**
     * Set
     */
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
    /**
     * Add
     */
    addTemplateWorker(state: StoreTemplateState, { template }: {template: TemplateWorker }) {
      if (template.id !== undefined) Vue.set(state.templatesWorker, template.id, template);
    },
    addTemplateAssignment(state: StoreTemplateState, { template }: { template: TemplateAssignment }) {
      if (template.id !== undefined) Vue.set(state.templatesAssignment, template.id, template);
    },
    addTemplateHIT(state: StoreTemplateState, { template }: { template: TemplateHIT }) {
      if (template.id !== undefined) Vue.set(state.templatesHIT, template.id, template);
    },
    addTemplateGlobal(state: StoreTemplateState, { template }: { template: TemplateGlobal }) {
      if (template.id !== undefined) Vue.set(state.templatesGlobal, template.id, template);
    },
    /**
     * Update
     */
    updateTemplateWorker(state: StoreTemplateState, { template }: {template: TemplateWorker }) {
      if (template.id !== undefined) Vue.set(state.templatesWorker, template.id, template);
    },
    updateTemplateAssignment(state: StoreTemplateState, { template }: { template: TemplateAssignment }) {
      if (template.id !== undefined) Vue.set(state.templatesAssignment, template.id, template);
    },
    updateTemplateHIT(state: StoreTemplateState, { template }: { template: TemplateHIT }) {
      if (template.id !== undefined) Vue.set(state.templatesHIT, template.id, template);
    },
    updateTemplateGlobal(state: StoreTemplateState, { template }: { template: TemplateGlobal }) {
      if (template.id !== undefined) Vue.set(state.templatesGlobal, template.id, template);
    },
    /**
     * Delete
     */
    deleteTemplateWorker(state: StoreTemplateState, { template }: {template: TemplateWorker }) {
      if (template.id !== undefined) Vue.delete(state.templatesWorker, template.id);
    },
    deleteTemplateAssignment(state: StoreTemplateState, { template }: { template: TemplateAssignment }) {
      if (template.id !== undefined) Vue.delete(state.templatesAssignment, template.id);
    },
    deleteTemplateHIT(state: StoreTemplateState, { template }: { template: TemplateHIT }) {
      if (template.id !== undefined) Vue.delete(state.templatesHIT, template.id);
    },
    deleteTemplateGlobal(state: StoreTemplateState, { template }: { template: TemplateGlobal }) {
      if (template.id !== undefined) Vue.delete(state.templatesGlobal, template.id);
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
