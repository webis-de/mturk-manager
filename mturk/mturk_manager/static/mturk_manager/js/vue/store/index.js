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

import { moduleMoney } from './modules/money.js';
import { moduleQualifications } from './modules/qualifications.js';
import { moduleWorkers } from './modules/workers.js';
import { moduleBatches } from './modules/batches.js';

export const store = new Vuex.Store({
    modules: {
        moduleMoney,
        moduleQualifications,
        moduleWorkers,
        moduleBatches,
    },
    state: {
        name_project: undefined,
        show_with_fee: true,
        show_progress_indicator: 0,

        url_project: undefined,
    },
    getters: {
        get_show_progress_indicator(state) {
            return state.show_progress_indicator > 0 ? true : false;
        }
    },
    mutations: {
        setNameProject(state, name_project) {
            state.name_project = name_project;
        },
        setUrlProject(state, url_project) {
            state.url_project = url_project;
        },
       
        set_show_with_fee(state, show) {
            state.show_with_fee = show;
        },
        set_show_progress_indicator(state, show) {
            state.show_progress_indicator += show == true ? 1 : -1;
        },
    },
    actions: {
        async init({commit, dispatch}) {
            const configElement = document.getElementById( 'config' );
            const config = JSON.parse( configElement.innerHTML );
            console.log(config);

            commit('setNameProject', config.name_project);

            commit('setUrlProject', config.url_project);

            commit('moduleBatches/set_url_api_assignments_real_approved', config.url_api_assignments_real_approved);

            commit('moduleMoney/setUrlApiGetBalance', config.url_api_get_balance);
            
            commit('moduleQualifications/set_url_api_qualifications', config.url_api_qualifications);

            commit('moduleWorkers/set_url_api_workers', config.url_api_workers);
        },
        async set_show_with_fee({commit, state}, show) {
            commit('set_show_with_fee', show);

        },
        async set_show_progress_indicator({commit, state}, show) {
            commit('set_show_progress_indicator', show);
        },
    }
})