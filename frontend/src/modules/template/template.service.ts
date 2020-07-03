import {
  queryCreateTemplateAssignment, queryCreateTemplateGlobal, queryCreateTemplateHIT, queryCreateTemplateWorker,
  queryDeleteTemplateAssignment,
  queryDeleteTemplateGlobal, queryDeleteTemplateHIT, queryDeleteTemplateWorker,
  queryTemplates,
  queryUpdateTemplateAssignment, queryUpdateTemplateGlobal, queryUpdateTemplateHIT,
  queryUpdateTemplateWorker,
} from '@/modules/template/template.graphql';
import { apolloClient } from '@/vue-apollo';
import { store } from '@/store/vuex';
import { TemplateWorker } from '@/modules/template/templateWorker.model';
import { TemplateAssignment } from '@/modules/template/templateAssignment.model';
import { TemplateHIT } from '@/modules/template/templateHIT.model';
import { TemplateGlobal } from '@/modules/template/templateGlobal.model';
import { TemplateBase } from '@/modules/template/templateBase.model';

class ClassServiceTemplates {
  async loadTemplates() {
    const response = await apolloClient.query({
      query: queryTemplates,
      variables: {
        project: store.getters['moduleProjects/get_project_current'].id,
      },
      fetchPolicy: 'no-cache',
    });

    return Promise.all([
      store.commit('moduleTemplates/setTemplatesWorker', {
        templates: TemplateWorker.prepareFromServerToStore(response.data.templatesWorker),
      }),
      store.commit('moduleTemplates/setTemplatesAssignment', {
        templates: TemplateAssignment.prepareFromServerToStore(response.data.templatesAssignment),
      }),
      store.commit('moduleTemplates/setTemplatesHIT', {
        templates: TemplateHIT.prepareFromServerToStore(response.data.templatesHit),
      }),
      store.commit('moduleTemplates/setTemplatesGlobal', {
        templates: TemplateGlobal.prepareFromServerToStore(response.data.templatesGlobal),
      }),
    ]);
  }

  async create({
    template,
  }) {
    let nameCommit;
    let nameMutation;
    let query;
    let cls: typeof TemplateBase;

    if (template instanceof TemplateAssignment) {
      nameCommit = 'createTemplateAssignment';
      nameMutation = 'createTemplateAssignment';
      query = queryCreateTemplateAssignment;
      cls = TemplateAssignment;
    }
    if (template instanceof TemplateHIT) {
      nameCommit = 'createTemplateHIT';
      nameMutation = 'createTemplateHit';
      query = queryCreateTemplateHIT;
      cls = TemplateHIT;
    }
    if (template instanceof TemplateGlobal) {
      nameCommit = 'createTemplateGlobal';
      nameMutation = 'createTemplateGlobal';
      query = queryCreateTemplateGlobal;
      cls = TemplateGlobal;
    }
    if (template instanceof TemplateWorker) {
      nameCommit = 'createTemplateWorker';
      nameMutation = 'createTemplateWorker';
      query = queryCreateTemplateWorker;
      cls = TemplateWorker;
    }

    const response = await apolloClient.query({
      query,
      variables: {
        template: template.extractBody(),
      },
      fetchPolicy: 'no-cache',
    });

    store.commit(`moduleTemplates/${nameCommit}`, {
      template: cls.parseFromServer(response.data[nameMutation].template),
    });
  }

  async update({
    templateCurrent, templateNew,
  }) {
    let nameCommit;
    let nameMutation;
    let query;
    let cls: typeof TemplateBase;

    if (templateCurrent instanceof TemplateAssignment) {
      nameCommit = 'updateTemplateAssignment';
      nameMutation = 'updateTemplateAssignment';
      query = queryUpdateTemplateAssignment;
      cls = TemplateAssignment;
    }
    if (templateCurrent instanceof TemplateHIT) {
      nameCommit = 'updateTemplateHIT';
      nameMutation = 'updateTemplateHit';
      query = queryUpdateTemplateHIT;
      cls = TemplateHIT;
    }
    if (templateCurrent instanceof TemplateGlobal) {
      nameCommit = 'updateTemplateGlobal';
      nameMutation = 'updateTemplateGlobal';
      query = queryUpdateTemplateGlobal;
      cls = TemplateGlobal;
    }
    if (templateCurrent instanceof TemplateWorker) {
      nameCommit = 'updateTemplateWorker';
      nameMutation = 'updateTemplateWorker';
      query = queryUpdateTemplateWorker;
      cls = TemplateWorker;
    }

    const response = await apolloClient.query({
      query,
      variables: {
        template: templateNew.extractBody(),
      },
      fetchPolicy: 'no-cache',
    });

    store.commit(`moduleTemplates/${nameCommit}`, {
      template: cls.parseFromServer(response.data[nameMutation].template),
    });
  }

  async delete({
    template,
  }: { template: TemplateBase }) {
    let nameCommit;
    let query;

    if (template instanceof TemplateAssignment) {
      nameCommit = 'deleteTemplateAssignment';
      query = queryDeleteTemplateAssignment;
    }
    if (template instanceof TemplateHIT) {
      nameCommit = 'deleteTemplateHIT';
      query = queryDeleteTemplateHIT;
    }
    if (template instanceof TemplateGlobal) {
      nameCommit = 'deleteTemplateGlobal';
      query = queryDeleteTemplateGlobal;
    }
    if (template instanceof TemplateWorker) {
      nameCommit = 'deleteTemplateWorker';
      query = queryDeleteTemplateWorker;
    }

    await apolloClient.query({
      query,
      variables: {
        id: template.id,
      },
      fetchPolicy: 'no-cache',
    });

    if (template instanceof TemplateAssignment || template instanceof TemplateHIT || template instanceof TemplateGlobal) {
      store.commit('moduleTemplates/updateWorkerTemplatesAfterDeletionOfRequesterTemplate', {
        template,
      });
    }

    store.commit(`moduleTemplates/${nameCommit}`, {
      template,
    });
  }
}

export const ServiceTemplates = new ClassServiceTemplates();
