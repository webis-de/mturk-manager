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

    console.log('templates', response);
  }
}

export const ServiceTemplates = new ClassServiceTemplates();
