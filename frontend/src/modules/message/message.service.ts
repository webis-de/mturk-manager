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
import { MessageBase } from '@/modules/message/MessageBase.model';
import { MessageReject } from '@/modules/message/MessageReject.model';
import {mutationCreateMessageReject, queryMessagesRejectSearch} from "@/modules/message/message.graphql";

class ClassServiceMessages {
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
      nameCommit = 'createTemplateAssignment';
      nameMutation = 'createTemplateAssignment';
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
    console.warn(response, 'response');
    return;
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

export const ServiceMessages = new ClassServiceMessages();
