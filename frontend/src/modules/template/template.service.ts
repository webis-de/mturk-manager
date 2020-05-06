import { queryTemplates } from '@/modules/template/template.graphql';
import { apolloClient } from '@/vue-apollo';
import { store } from '@/store/vuex';

class ClassServiceTemplates {
  async loadTemplates() {
    const response = await apolloClient.query({
      query: queryTemplates,
      variables: {
        project: store.getters['moduleProjects/get_project_current'].id,
      },
      // fetchPolicy: 'no-cache',
    });

    store.dispatch('moduleTemplates/setTemplatesWorker', {
      templates: response.data.templatesWorker,
    });
    store.dispatch('moduleTemplates/setTemplatesAssignment', {
      templates: response.data.templatesAssignment,
    });
    store.dispatch('moduleTemplates/setTemplatesHIT', {
      templates: response.data.templatesHit,
    });
    store.dispatch('moduleTemplates/setTemplatesGlobal', {
      templates: response.data.templatesGlobal,
    });
    console.log('templates', response.data);
  }
}

export const ServiceTemplates = new ClassServiceTemplates();
