import _ from 'lodash';
import Vue from 'vue';
import baseModule from '@/store/modules/base.module';
import { classesHeaders } from '@/helpers';
import { MessageReject } from '@/modules/message/messageReject.model';

interface StoreMessageState {
  messagesReject: { [key: string]: MessageReject};
}

export const moduleMessages = _.merge({}, baseModule, {
  namespaced: true,
  state: {
    messagesReject: null,

    paginationMessagesReject: {
      rowsPerPage: 5,
      sortBy: 'message',
      descending: true,
    },

    // columns
    arrayColumns: [
      {
        text: 'Message',
        value: 'message',
        classes: ['text-left'],
      },
      {
        text: 'Usages',
        value: 'count_usage',
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
      message: true,
      actions: true,
    },
  },
  getters: {
    messagesReject(state: StoreMessageState): MessageReject[] | null {
      if (state.messagesReject === null) return null;

      return Object.values(state.messagesReject);
    },
  },
  mutations: {
    /**
     * Set
     */
    setMessagesReject(state: StoreMessageState, { messages }: {messages: { [key: string]: MessageReject}}) {
      state.messagesReject = messages;
    },
    /**
     * Create
     */
    createMessageReject(state: StoreMessageState, { message }: {message: MessageReject }) {
      if (message.id !== undefined) Vue.set(state.messagesReject, message.id, message);
    },
    /**
     * Update
     */
    updateMessageReject(state: StoreMessageState, { message }: {message: MessageReject }) {
      if (message.id !== undefined) Vue.set(state.messagesReject, message.id, message);
    },
    /**
     * Delete
     */
    deleteMessageReject(state: StoreMessageState, { message }: {message: MessageReject }) {
      if (message.id !== undefined) Vue.delete(state.messagesReject, message.id);
    },
  },
  actions: {
    async init({ dispatch }) {
      await Promise.all([
        /**
         * init pagination
         */
        dispatch('loadState', {
          nameLocalStorage: 'pagination_messages_reject',
          nameState: 'paginationMessagesReject',
        }),
      ]);
    },
  },
});
