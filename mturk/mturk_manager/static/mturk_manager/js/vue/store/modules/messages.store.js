import _ from 'lodash';
import Vue from 'vue';
import baseModule from './base.module';

export const moduleMessages = _.merge({}, baseModule, {
  namespaced: true,
  state: {
    // urls
    urlApiMessagesReject: undefined,
    urlApiMessagesApprove: undefined,
    urlApiMessagesReason: undefined,
    urlApiProjectsMessagesReject: undefined,
    urlApiProjectsMessagesApprove: undefined,
    urlApiProjectsMessagesReason: undefined,

    object_messages_reject: null,

    // arrays
    arrayItemsReject: null,
    arrayItemsApprove: null,
    arrayItemsReason: null,

    // pagination
    paginationMessagesReject: {
      rowsPerPage: 5,
      sortBy: 'message',
      descending: true,
    },
    paginationMessagesApprove: {
      rowsPerPage: 5,
      sortBy: 'message',
      descending: true,
    },
    paginationMessagesReason: {
      rowsPerPage: 5,
      sortBy: 'message',
      descending: true,
    },

    // columns
    arrayColumns: [
      {
        text: 'Message',
        value: 'message',
        classes: ['text-xs-left'],
      },
      {
        text: '',
        value: 'actions',
        classes: ['text-xs-right'],
      },
    ],

    array_columns_selected: [
      'message',
      'actions',
    ],
  },
  getters: {
    get_list_messages_reject: state => _.orderBy(state.object_messages_reject, 'count_usage', 'desc'),
  },
  mutations: {
    set_messages_reject(state, data) {
      state.object_messages_reject = {};

      _.forEach(data, (message_reject) => {
        // const object_project = new Project(message_reject);
        Vue.set(
          state.object_messages_reject,
          message_reject.message,
          message_reject,
        );
      });
    },
    add_message_reject(state, { message_reject }) {
      Vue.set(
        state.object_messages_reject,
        message_reject.message,
        message_reject,
      );
    },
    set_urls(state, config) {
      state.urlApiMessagesReject = config.url_api_messages_reject;
      state.urlApiMessagesApprove = config.url_api_messages_approve;
      state.urlApiMessagesReason = config.url_api_messages_reason;
      state.urlApiProjectsMessagesReject = config.url_api_projects_messages_reject;
      state.urlApiProjectsMessagesApprove = config.url_api_projects_messages_approve;
      state.urlApiProjectsMessagesReason = config.url_api_projects_messages_reason;
    },
  },
  actions: {},
});
