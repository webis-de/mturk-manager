import { apolloClient } from '@/vue-apollo';
import { store } from '@/store/vuex';
import { TemplateBase } from '@/modules/template/templateBase.model';
import { MessageBase } from '@/modules/message/messageBase.model';
import { MessageReject } from '@/modules/message/messageReject.model';
import {
  mutationCreateMessageReject, mutationDeleteMessageReject,
  queryMessagesReject,
  queryMessagesRejectSearch,
} from '@/modules/message/message.graphql';

class ClassServiceMessages {
  async loadMessages() {
    const response = await apolloClient.query({
      query: queryMessagesReject,
      variables: {
        project: store.getters['moduleProjects/get_project_current'].id,
      },
      fetchPolicy: 'no-cache',
    });

    return Promise.all([
      store.commit('moduleMessages/setMessagesReject', {
        messages: MessageReject.prepareFromServerToStore(response.data.messagesReject),
      }),
    ]);
  }

  async search({ message, cls }: { message: string; cls: typeof MessageBase}) {
    let query;

    switch (cls) {
      case MessageReject:
        query = queryMessagesRejectSearch;
        break;
      default:
        query = queryMessagesRejectSearch;
    }
    const response = await apolloClient.query({
      query,
      variables: {
        message,
        // project: store.getters['moduleProjects/get_project_current'].id,
      },
      fetchPolicy: 'no-cache',
    });

    return response.data.searchMessagesReject;
    // return Promise.all([
    //   store.commit('moduleTemplates/setTemplatesWorker', {
    //     templates: TemplateWorker.prepareFromServerToStore(response.data.templatesWorker),
    //   }),
    //   store.commit('moduleTemplates/setTemplatesAssignment', {
    //     templates: TemplateAssignment.prepareFromServerToStore(response.data.templatesAssignment),
    //   }),
    //   store.commit('moduleTemplates/setTemplatesHIT', {
    //     templates: TemplateHIT.prepareFromServerToStore(response.data.templatesHit),
    //   }),
    //   store.commit('moduleTemplates/setTemplatesGlobal', {
    //     templates: TemplateGlobal.prepareFromServerToStore(response.data.templatesGlobal),
    //   }),
    // ]);
  }

  async create({
    message,
  }: { message: MessageBase }) {
    let nameCommit;
    let nameMutation;
    let query;
    let cls: typeof TemplateBase;

    if (message instanceof MessageReject) {
      nameCommit = 'createMessageReject';
      nameMutation = 'createMessageReject';
      query = mutationCreateMessageReject;
      cls = MessageReject;
    }

    const response = await apolloClient.query({
      query,
      variables: {
        message: message.extractBody(),
      },
      fetchPolicy: 'no-cache',
    });

    store.commit(`moduleMessages/${nameCommit}`, {
      message: cls.parseFromServer(response.data[nameMutation].message),
    });
  }

  async delete({
    message,
  }: { message: MessageBase }) {
    let nameCommit;
    let query;

    if (message instanceof MessageReject) {
      nameCommit = 'deleteMessageReject';
      query = mutationDeleteMessageReject;
    }

    await apolloClient.query({
      query,
      variables: {
        id: message.id,
      },
      fetchPolicy: 'no-cache',
    });

    store.commit(`moduleMessages/${nameCommit}`, {
      message,
    });
  }
}

export const ServiceMessages = new ClassServiceMessages();
