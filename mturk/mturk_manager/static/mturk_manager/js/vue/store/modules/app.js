import localforage from 'localforage';

export const module_app = {
  namespaced: true,
  state: {
    url_api: null,
    token_instance: null,
    use_sandbox: true,
    version_api: null,
    version_app: 1.01,
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
  },
  actions: {
    async load_credentials({ commit }) {
      const url_api = await localforage.getItem('url_api');
      const token_instance = await localforage.getItem('token_instance');

      if (url_api === null || token_instance === null) {
        return false;
      }

      commit('set_url_api', url_api);
      commit('set_token_instance', token_instance);
      return true;
    },
    async init({ commit, dispatch }, config) {
      let use_sandbox = await localforage.getItem('use_sandbox');
      if (use_sandbox === null) {
        use_sandbox = true;
      }
      commit('set_use_sandbox', use_sandbox);

      commit('version_api', config.version_api);

      commit('moduleAssignments/set_urls', config.paths, { root: true });
      commit('moduleBatches/set_urls', config.paths, { root: true });
      commit('moduleHITs/set_urls', config.paths, { root: true });
      commit('moduleKeywords/set_urls', config.paths, { root: true });
      commit('moduleMessagesReject/set_urls', config.paths, { root: true });
      commit('moduleProjects/set_urls', config.paths, { root: true });
      commit('moduleWorkers/set_urls', config.paths, { root: true });
      commit('module_finances/set_urls', config.paths, { root: true });
      commit('moduleSettingsBatch/setUrls', config.paths, { root: true });

      dispatch('moduleBatches/init', null, { root: true });
      dispatch('moduleHITs/init', null, { root: true });
      dispatch('moduleAssignments/init', null, { root: true });
      dispatch('moduleWorkers/init', null, { root: true });
    },
    async set_credentials({ commit }, { url, token }) {
      commit('set_url_api', url);
      commit('set_token_instance', token);

      await localforage.setItem('url_api', url);
      await localforage.setItem('token_instance', token);
    },
    async set_use_sandbox({ commit, state }, use_sandbox) {
      commit('set_use_sandbox', use_sandbox);
      localforage.setItem('use_sandbox', use_sandbox);
    },
  },
};
