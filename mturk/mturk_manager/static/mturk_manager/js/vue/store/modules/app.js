import Vue from 'vue';
import localforage from 'localforage';
import _ from 'lodash';

import baseModule from './base.module';

export const module_app = _.merge({}, baseModule, {
  state: {
    url_api: null,
    token_instance: null,
    use_sandbox: true,
    version_api: null,
    version: '1.3.0',
    changelog: [],
    versionSeen: null,
  },
  getters: {
    has_credentials(state) {
      return state.url_api !== null && state.token_instance !== null;
    },
  },
  mutations: {
    set_url_api(state, url_api) {
      state.url_api = url_api;
    },
    set_token_instance(state, token_instance) {
      state.token_instance = token_instance;
    },
    set_use_sandbox(state, use_sandbox) {
      state.use_sandbox = use_sandbox;
    },
    version_api(state, version_api) {
      state.version_api = version_api;
    },
    setReleaseBody(state, { idTag, body }) {
      const release = state.changelog.find(release => release.id === idTag);
      if(release !== undefined) {
        Vue.set(release, 'body', body);
      }
    },
  },
  actions: {
    async load_credentials({ getters, dispatch }) {
      await dispatch('loadState', {
        nameLocalStorage: 'url_api',
        nameState: 'url_api',
      });

      await dispatch('loadState', {
        nameLocalStorage: 'token_instance',
        nameState: 'token_instance',
      });

      return getters.has_credentials;
    },
    async init({ commit, dispatch }, config) {
      let use_sandbox = await localforage.getItem('use_sandbox');
      if (use_sandbox === null) {
        use_sandbox = true;
      }
      commit('set_use_sandbox', use_sandbox);

      commit('version_api', config.version);

      dispatch('loadState', {
        nameLocalStorage: 'changelog',
        nameState: 'changelog',
        objectStateDefault: [],
      });

      dispatch('loadState', {
        nameLocalStorage: 'version_seen',
        nameState: 'versionSeen',
      });


      commit('moduleAssignments/set_urls', config.paths, { root: true });
      commit('moduleBatches/set_urls', config.paths, { root: true });
      commit('moduleHITs/set_urls', config.paths, { root: true });
      commit('moduleKeywords/set_urls', config.paths, { root: true });
      commit('moduleMessages/set_urls', config.paths, { root: true });
      commit('moduleProjects/set_urls', config.paths, { root: true });
      commit('moduleWorkers/set_urls', config.paths, { root: true });
      commit('module_finances/set_urls', config.paths, { root: true });
      commit('moduleSettingsBatch/setUrls', config.paths, { root: true });
      commit('moduleTemplates/setUrls', config.paths, { root: true });

      await Promise.all([
        dispatch('moduleBatches/init', null, { root: true }),
        dispatch('moduleHITs/init', null, { root: true }),
        dispatch('moduleAssignments/init', null, { root: true }),
        dispatch('moduleWorkers/init', null, { root: true }),
        dispatch('moduleSettingsBatch/init', null, { root: true }),
        dispatch('moduleTemplates/init', null, { root: true }),
        dispatch('moduleMessages/init', null, { root: true }),
      ]);
    },
    async set_use_sandbox({ commit }, use_sandbox) {
      commit('set_use_sandbox', use_sandbox);
      localforage.setItem('use_sandbox', use_sandbox);
    },
    async setReleaseBody({ state, commit }, data) {
      commit('setReleaseBody', data);

      await localforage.setItem('changelog', state.changelog);
    },
  },
});
