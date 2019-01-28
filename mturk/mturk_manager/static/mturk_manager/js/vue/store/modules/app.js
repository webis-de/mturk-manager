import localforage from "localforage";

export const module_app = {
	namespaced: true,
	state: {
        url_api: null,
        token_instance: null,
    },
    getters: {
        has_credentials(state) {
            return state.url_api !== null && state.token_instance !== null;
        }
    },
    mutations: {
        set_url_api(state, url_api) { state.url_api = url_api; },
        set_token_instance(state, token_instance) { state.token_instance = token_instance; },
    },
    actions: {
        async init({commit}) {
            const url_api = await localforage.getItem('url_api');
            const token_instance = await localforage.getItem('token_instance');

            if(url_api === null || token_instance === null) {
                return false;
            }

            commit('set_url_api', url_api);
            commit('set_token_instance', token_instance);

            return true;
        },
        async set_credentials({}, {url, token}) {
            await localforage.setItem('url_api', url);
            await localforage.setItem('token_instance', token);
        }
    }
};