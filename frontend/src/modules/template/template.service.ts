import { queryTemplates } from '@/modules/template/template.graphql';
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
}

export const ServiceTemplates = new ClassServiceTemplates();
