import Vuex from 'vuex';
// import Vue from 'vue/dist/vue.common';
import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import _ from 'lodash';

import VueCookies from 'vue-cookies'
Vue.use(Vuex)
Vue.use(VueCookies)
Vue.use(VueAxios, axios)

import { moduleProjects } from './modules/projects.js';
import { moduleMoney } from './modules/money.js';
import { moduleQualifications } from './modules/qualifications.js';
import { moduleWorkers } from './modules/workers.js';
import { moduleBatches } from './modules/batches.js';
import { moduleHITs } from './modules/hits.js';
import { moduleKeywords } from './modules/keywords.js';

export const store = new Vuex.Store({
    modules: {
        moduleProjects,
        moduleMoney,
        moduleQualifications,
        moduleWorkers,
        moduleBatches,
        moduleHITs,
        moduleKeywords,
    },
    state: {
        has_loaded_projects: false,
        token_instance: undefined,
        token_csrf: undefined,
        show_with_fee: true,
        show_progress_indicator: 0,
        // use_sandbox: false,
        use_sandbox: true,
    },
    getters: {
        get_show_progress_indicator(state, getters, rootState) {
            return state.show_progress_indicator > 0 ? true : false;
        },
        get_url_api: (state, getters) => ({url, use_sandbox, value}) => {
            if(value != undefined)
            {
                url += `/${value}`;
            }

            if(use_sandbox === false) {
                url += '?use_sandbox=false&';
            } else {
                url += '?';
            }

            url = url.replace('PLACEHOLDER_SLUG_PROJECT', getters['moduleProjects/get_project_current'].slug);

            return url;
        },
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
        set_use_sandbox(state, use_sandbox) {
            state.use_sandbox = use_sandbox;
        },
        set_show_progress_indicator(state, show) {
            state.show_progress_indicator += show == true ? 1 : -1;
        },
    },
    actions: {
        async init({state, commit, dispatch}) {
            const configElement = document.getElementById( 'config' );
            const config = JSON.parse( configElement.innerHTML );
            console.log(config);

            commit('set_token_instance', config.token_instance);
            commit('set_token_csrf', config.token_csrf);

            // commit('setUrlProject', config.url_project);

            commit('moduleMoney/setUrlApiGetBalance', config.url_api_get_balance);
            
            commit('moduleQualifications/set_url_api_qualifications', config.url_api_qualifications);
            // commit('moduleQualifications/set_url_api_qualification', config.url_api_qualification);

            commit('moduleWorkers/set_url_api_workers', config.url_api_workers);
            commit('moduleWorkers/set_url_api_global_db', config.url_api_global_db);

            commit('moduleProjects/set_urls', config);

            // commit('moduleProjects/set_url_api_projects', config.url_api_projects);
            // commit('moduleProjects/set_slug_project_current', config.slug_project_current);

            commit('moduleBatches/set_urls', config);
            
            commit('moduleKeywords/set_urls', config);

            await dispatch('moduleProjects/load_projects');
            state.has_loaded_projects = true;
        },
        async set_show_with_fee({commit, state}, show) {
            commit('set_show_with_fee', show);
        },
        async set_show_progress_indicator({commit, state}, show) {
            commit('set_show_progress_indicator', show);
        },
        async set_use_sandbox({commit, state}, use_sandbox) {
            commit('set_use_sandbox', use_sandbox);
        },
        async make_request({commit, state}, {url, method, data}) {
            let response = undefined;
            let function_axios = undefined;

            let config = {
                method: method,
                url: url,
                data: JSON.stringify(data),
                headers: {
                    Authorization: `Token ${state.token_instance}`,
                    "Content-Type": 'application/json',
                }
            };

            await axios(config).then(
                    r => {
                        response = r;
                    }
                );

            return response;
        },
    }
})