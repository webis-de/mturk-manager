import Vuex from 'vuex';
import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import _ from 'lodash';
import Papa from 'papaparse';

Vue.use(Vuex)
Vue.use(VueAxios, axios)

import { moduleMoney } from './modules/money.js';

export const store = new Vuex.Store({
    modules: {
        moduleMoney
    },
    state: {
        name_project: undefined,
        url_project: undefined,
        url_api_get_balance: undefined,
        url_api_assignments_real_approved: undefined,
        object_batches: {},
    },
    getters: {
        list_batches: state => {
            return _.orderBy(state.object_batches, ['datetime_creation'], ['desc']);
        },
        list_hits_for_csv: state => {
            const list_hits = [];
            _.forIn(state.object_batches, function(batch, id_batch) {
                _.forEach(batch.hits, function(hit){
                    list_hits.push([
                        hit.id_hit,
                        (hit.count_assignments * batch.reward).toFixed(2),
                    ]);
                });
            });
            return list_hits;
        },
    },
    mutations: {
        setNameProject(state, name_project) {
            state.name_project = name_project;
        },
        setUrlProject(state, url_project) {
            state.url_project = url_project;
        },
        setBatchesAndHits(state, {list_hits, dict_batches}) {
            // set batches
            _.forIn(dict_batches, function(batch, id_batch) {
                state.object_batches[id_batch] = batch;
                state.object_batches[id_batch]['hits'] = [];

            });

            // set hits
            _.forEach(list_hits, function(hit){
                // console.log(Date.parse(hit.datetime_creation));
                hit.datetime_creation = new Date(hit.datetime_creation);

                state.object_batches[hit.id_batch].hits.push(hit);
            });


            _.forIn(state.object_batches, function(batch, id_batch) {
                // datetime of last hit is created time of batch
                batch.datetime_creation = batch.hits[0].datetime_creation;

                batch.number_assignments_approved = _.sumBy(
                    batch.hits, 'count_assignments'
                );

                batch.money_spent = batch.number_assignments_approved * batch.reward
            });

            console.log(state.object_batches)

            state.object_batches = dict_batches;
        },
        setObjectBatches(state, dict_batches) {
            for(let id_batch in dict_batches) {
                state.object_batches[id_batch] = dict_batches[id_batch];
            };
            state.object_batches = dict_batches;
        },
        setUrlApiGetBalance(state, url_new) {
            state.url_api_get_balance = url_new;
        },
        setUrlApiAssignmentsRealApproved(state, url_new) {
            state.url_api_assignments_real_approved = url_new;
        },
    },
    actions: {
        async init({commit, dispatch}) {
            const configElement = document.getElementById( 'config' );
            const config = JSON.parse( configElement.innerHTML );
            console.log(config);
 
            commit('setUrlApiGetBalance', config.url_api_get_balance);
            commit('setUrlApiAssignmentsRealApproved', config.url_api_assignments_real_approved);
            commit('setNameProject', config.name_project);
            commit('setUrlProject', config.url_project);

            dispatch('moduleMoney/update_balance');
            dispatch('refresh_data');
        },
        async refresh_data({commit, state}) {
            await axios.get(state.url_api_assignments_real_approved)
            .then(response => {
                commit('setBatchesAndHits', response.data);
            })
        },
    }
})