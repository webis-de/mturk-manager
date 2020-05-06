import { queryTemplates } from '@/modules/template/template.graphql';
import { apolloClient } from '@/vue-apollo';

class ClassServiceTemplates {
  async loadTemplates() {
    const response = await apolloClient.query({
      query: queryTemplates,
      // fetchPolicy: 'no-cache',
    });

    console.log('templates', response);
  }
}

export const ServiceTemplates = new ClassServiceTemplates();
