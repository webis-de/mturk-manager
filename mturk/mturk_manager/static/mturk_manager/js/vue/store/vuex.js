import Vuex from 'vuex';
import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import _ from 'lodash';
import localforage from 'localforage';

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
import { moduleAssignments } from './modules/assignments.js';
import { moduleKeywords } from './modules/keywords.js';
import { moduleMessagesReject } from './modules/messages_reject.js';
import {Service_Endpoint} from "../services/service_endpoint";
// import { router } from './index.js';

export const store = new Vuex.Store({
    modules: {
        moduleProjects,
        moduleMoney,
        moduleQualifications,
        moduleWorkers,
        moduleBatches,
        moduleHITs,
        moduleAssignments,
        moduleKeywords,
        moduleMessagesReject,
    },
    state: {
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
            if(value !== undefined)
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
        get_url: (state) => (url, module) => {
            return state[module][url];
        },
        get_use_sandbox(state) {
            return state.use_sandbox;
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
            localforage.setItem('use_sandbox', use_sandbox);
        },
        set_show_progress_indicator(state, show) {
            state.show_progress_indicator += show === true ? 1 : -1;
        },
        // set_urls(state, config) {
        // },
    },
    actions: {
        async init({state, commit, dispatch}) {
            const configElement = document.getElementById( 'config' );
            const config = JSON.parse( configElement.innerHTML );
            console.log(config);

            commit('set_token_instance', config.token_instance);
            commit('set_token_csrf', config.token_csrf);

            let use_sandbox = await localforage.getItem('use_sandbox');
            if(use_sandbox === null)
            {
                use_sandbox = true;
            }
            commit('set_use_sandbox', use_sandbox);

            // commit('setUrlProject', config.url_project);

            commit('moduleMoney/setUrlApiGetBalance', config.url_api_get_balance);
            
            commit('moduleQualifications/set_url_api_qualifications', config.url_api_qualifications);
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
    }
})