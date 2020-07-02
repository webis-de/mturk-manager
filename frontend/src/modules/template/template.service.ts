import {
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

    const templatesAssignment = this.processData({ data: response.data.templatesAssignment, Cls: TemplateAssignment });
    const templatesHIT = this.processData({ data: response.data.templatesHit, Cls: TemplateHIT });
    const templatesGlobal = this.processData({ data: response.data.templatesGlobal, Cls: TemplateGlobal });


    const templatesWorker: TemplateWorker[] = response.data.templatesWorker.map((item: {}) => {
      item.templateAssignment = item.templateAssignment !== null ? templatesAssignment[item.templateAssignment.id] : null;
      item.templateHIT = item.templateHit !== null ? templatesHIT[item.templateHit.id] : null;
      item.templateGlobal = item.templateGlobal !== null ? templatesGlobal[item.templateGlobal.id] : null;
      // item.templateOriginal = item.templateOriginal !== null ? templatesOriginal[item.templateOriginal.id] : null;
      return new TemplateWorker(item);
    });

    console.warn(templatesWorker, 'templatesWorker');

    return Promise.all([
      store.dispatch('moduleTemplates/setTemplatesWorker', {
        templates: templatesWorker.reduce((obj, template) => {
          obj[template.id as string] = template;
          return obj;
        }, {} as {[key: string]: TemplateWorker}),
      }),
      store.dispatch('moduleTemplates/setTemplatesAssignment', {
        templates: templatesAssignment,
      }),
      store.dispatch('moduleTemplates/setTemplatesHIT', {
        templates: templatesHIT,
      }),
      store.dispatch('moduleTemplates/setTemplatesGlobal', {
        templates: templatesGlobal,
      }),
    ]);
  }

  processData({ data, Cls }: { data: {}[]; Cls: new ({}) => TemplateBase }): {[key: string]: TemplateBase} {
    const templates: TemplateBase[] = data.map((item: {}) => new Cls(item));

    return templates.reduce((obj, template) => {
      obj[template.id as string] = template;
      return obj;
    }, {} as {[key: string]: TemplateBase});
  }

  async update({
    templateCurrent, templateNew,
  }) {
    let nameCommit;
    let nameMutation;
    let query;
    let cls: TemplateBase;

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
      template: new cls(response.data[nameMutation].template),
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

    store.commit(`moduleTemplates/${nameCommit}`, {
      template,
    });
  }
}

export const ServiceTemplates = new ClassServiceTemplates();
