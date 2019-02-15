import Vuex from 'vuex';
import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import localforage from 'localforage';

import VueCookies from 'vue-cookies';

import { moduleProjects } from './modules/projects.js';
import { moduleQualifications } from './modules/qualifications.js';
import { moduleWorkers } from './modules/workers.js';
import { moduleBatches } from './modules/batches.js';
import { moduleHITs } from './modules/hits.js';
import { moduleAssignments } from './modules/assignments.js';
import { moduleKeywords } from './modules/keywords.js';
import { moduleMessagesReject } from './modules/messages_reject.js';
import { module_app } from './modules/app';
import { module_finances } from './modules/finances';

Vue.use(Vuex);
Vue.use(VueCookies);
Vue.use(VueAxios, axios);

export const store = new Vuex.Store({
  modules: {
    module_app,
    moduleProjects,
    module_finances,
    moduleQualifications,
    moduleWorkers,
    moduleBatches,
    moduleHITs,
    moduleAssignments,
    moduleKeywords,
    moduleMessagesReject,
  },
  state: {
    token_csrf: undefined,
    show_with_fee: true,
    show_progress_indicator: 0,
  },
  getters: {
    get_url_api(state) {
      return state.url_api;
    },
    get_token_instance(state) {
      return state.token_instance;
    },

    get_show_progress_indicator(state, getters, rootState) {
      return state.show_progress_indicator > 0;
    },
    // get_url_api: (state, getters) => ({url, use_sandbox, value}) => {
    //     if(value !== undefined)
    //     {
    //         url += `/${value}`;
    //     }
    //
    //     if(use_sandbox === false) {
    //         url += '?use_sandbox=false&';
    //     } else {
    //         url += '?';
    //     }
    //
    //     url = url.replace('PLACEHOLDER_SLUG_PROJECT', getters['moduleProjects/get_project_current'].slug);
    //
    //     return url;
    // },
    get_url: state => (url, module) => state[module][url],
  },
  mutations: {
    set_token_csrf(state, token_csrf) {
      state.token_csrf = token_csrf;
    },
    set_token_instance(state, token_instance) {
      state.token_instance = token_instance;
    },
    set_show_with_fee(state, show) {
      state.show_with_fee = show;
    },
    set_show_progress_indicator(state, show) {
      state.show_progress_indicator += show === true ? 1 : -1;
    },
    // set_urls(state, config) {
    // },
  },
  actions: {
    async init({ state, commit, dispatch }) {
      state.url_api = await localforage.getItem('url_api');
      state.token_instance = await localforage.getItem('token_instance');

      const configElement = document.getElementById('config');
      const config = JSON.parse(configElement.innerHTML);
      console.log(config);

      commit('set_token_instance', config.token_instance);
      commit('set_token_csrf', config.token_csrf);

      // commit('setUrlProject', config.url_project);

      commit('module_finances/set_urls', config);

      commit(
        'moduleQualifications/set_url_api_qualifications',
        config.url_api_qualifications,
      );
      // commit('moduleQualifications/set_url_api_qualification', config.url_api_qualification);

      // commit('set_urls', config);

      commit('moduleWorkers/set_urls', config);
      // commit('moduleWorkers/set_url_api_global_db', config.url_api_global_db);

      commit('moduleProjects/set_urls', config);

      // commit('moduleProjects/set_url_api_projects', config.url_api_projects);
      // commit('moduleProjects/set_slug_project_current', config.slug_project_current);

      commit('moduleBatches/set_urls', config);
      commit('moduleHITs/set_urls', config);
      commit('moduleAssignments/set_urls', config);

      commit('moduleKeywords/set_urls', config);
      commit('moduleMessagesReject/set_urls', config);

      dispatch('moduleBatches/init');
      dispatch('moduleHITs/init');
      dispatch('moduleAssignments/init');
    },
    async set_show_with_fee({ commit, state }, show) {
      commit('set_show_with_fee', show);
    },
    async set_show_progress_indicator({ commit, state }, show) {
      commit('set_show_progress_indicator', show);
    },
  },
});
