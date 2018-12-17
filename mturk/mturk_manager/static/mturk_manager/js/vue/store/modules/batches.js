import Vuex from 'vuex';
// import Vue from 'vue/dist/vue.common';
import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import _ from 'lodash';
import Batch from '../../classes/batch.js';
import HIT from '../../classes/hit.js';
import {Service_Endpoint} from '../../services/service_endpoint';

import VueCookies from 'vue-cookies'
Vue.use(Vuex)
Vue.use(VueCookies)
Vue.use(VueAxios, axios)

export const moduleBatches = {
	namespaced: true,
	state: {
        object_batches: null,
		object_batches_sandbox: null,

        array_batches: null,
        array_batches_sandbox: null,

        url_api_assignments_real_approved: undefined,

        url_api_projects_batches: undefined,
        url_api_projects_batches_download: undefined,
        url_api_projects_batches_download_info: undefined,

        object_batches_selected: {},

        object_csv_parsed: undefined,
        is_syncing_mturk: false,
	},
    getters: {
	    get_object_batches_selected: (state) => {
	        return state.object_batches_selected;
        },
        get_array_batches: (state, getters, rootState) => (use_sandbox=undefined) => {
            if(use_sandbox == undefined)
            {
                return rootState.use_sandbox ? state.array_batches_sandbox : state.array_batches;
            } else {
                return use_sandbox ? state.array_batches_sandbox : state.array_batches;
            }
        },
        is_valid_csv: (state) => {
            if(state.object_csv_parsed == undefined) 
            {
                return false;
            } else {
                return state.object_csv_parsed.errors.length == 0;
            }
        },
        get_object_csv_parsed: (state) => {
            return state.object_csv_parsed;
        },
        // get_object_batches: (state, getters, rootState) => {
        //     return rootState.use_sandbox ? state.object_batches_sandbox : state.object_batches;
        // },

        list_hits_for_csv: state => {
            const list_hits = [];
            _.forIn(state.object_batches, function(batch, id_batch) {
                _.forEach(batch.hits, function(hit){
                    list_hits.push([
                        hit.id_hit,
                        (hit.count_assignments * batch.reward).toFixed(2),
                        id_batch,
                    ]);
                });
            });
            return list_hits;
        },
        get_is_syncing_mturk: (state) => {
            return state.is_syncing_mturk;
        },
    },
	mutations: {
        // setBatchesAndHits_sandbox(state, {list_hits, dict_batches}) {
        //     // set batches
        //     state.object_batches_sandbox = {};
        //     _.forIn(dict_batches, function(batch, id_batch) {
        //         state.object_batches_sandbox[id_batch] = batch;
        //         state.object_batches_sandbox[id_batch]['hits'] = [];

        //     });

        //     // set hits
        //     _.forEach(list_hits, function(hit){
        //         // console.log(Date.parse(hit.datetime_creation));
        //         hit.datetime_creation = new Date(hit.datetime_creation);

        //         state.object_batches_sandbox[hit.id_batch].hits.push(hit);
        //     });


        //     _.forIn(state.object_batches_sandbox, function(batch, id_batch) {
        //         // datetime of last hit is created time of batch
        //         batch.datetime_creation = batch.hits[0].datetime_creation;

        //         batch.count_assignments_approved = _.sumBy(
        //             batch.hits, 'count_assignments_approved'
        //         );
        //         batch.count_assignments_rejected = _.sumBy(
        //             batch.hits, 'count_assignments_rejected'
        //         );

        //         batch.count_assignments_total =  batch.hits.length * batch.count_assignments_per_hit;

        //         batch.money_spent_without_fee = batch.count_assignments_approved * batch.reward;
        //         if(batch.count_assignments_per_hit < 10) {
        //             batch.money_spent_with_fee = batch.money_spent_without_fee * 1.2;
        //         } else {
        //             batch.money_spent_with_fee = batch.money_spent_without_fee * 1.4;
        //         }

        //         batch.money_spent_max_without_fee = batch.count_assignments_total * batch.reward;
        //         if(batch.count_assignments_per_hit < 10) {
        //             batch.money_spent_max_with_fee = batch.money_spent_max_without_fee * 1.2;
        //         } else {
        //             batch.money_spent_max_with_fee = batch.money_spent_max_without_fee * 1.4;
        //         }

        //         batch.money_not_spent_without_fee = batch.count_assignments_rejected * batch.reward;
        //         if(batch.count_assignments_per_hit < 10) {
        //             batch.money_not_spent_with_fee = batch.money_not_spent_without_fee * 1.2;
        //         } else {
        //             batch.money_not_spent_with_fee = batch.money_not_spent_without_fee * 1.4;
        //         }
        //     });

        //     // console.log(state.object_batches_sandbox)

        //     state.object_batches_sandbox = dict_batches;
        // },
        // setBatchesAndHits(state, {list_hits, dict_batches}) {
        //     // set batches
        //     state.object_batches = {};
        //     _.forIn(dict_batches, function(batch, id_batch) {
        //         state.object_batches[id_batch] = batch;
        //         state.object_batches[id_batch]['hits'] = [];

        //     });

        //     // set hits
        //     _.forEach(list_hits, function(hit){
        //         // console.log(Date.parse(hit.datetime_creation));
        //         hit.datetime_creation = new Date(hit.datetime_creation);

        //         state.object_batches[hit.id_batch].hits.push(hit);
        //     });


        //     _.forIn(state.object_batches, function(batch, id_batch) {
        //         // datetime of last hit is created time of batch
        //         batch.datetime_creation = batch.hits[0].datetime_creation;

        //         batch.count_assignments_approved = _.sumBy(
        //             batch.hits, 'count_assignments_approved'
        //         );
        //         batch.count_assignments_rejected = _.sumBy(
        //             batch.hits, 'count_assignments_rejected'
        //         );

        //         batch.count_assignments_total =  batch.hits.length * batch.count_assignments_per_hit;

        //         batch.money_spent_without_fee = batch.count_assignments_approved * batch.reward;
        //         if(batch.count_assignments_per_hit < 10) {
        //             batch.money_spent_with_fee = batch.money_spent_without_fee * 1.2;
        //         } else {
        //             batch.money_spent_with_fee = batch.money_spent_without_fee * 1.4;
        //         }

        //         batch.money_spent_max_without_fee = batch.count_assignments_total * batch.reward;
        //         if(batch.count_assignments_per_hit < 10) {
        //             batch.money_spent_max_with_fee = batch.money_spent_max_without_fee * 1.2;
        //         } else {
        //             batch.money_spent_max_with_fee = batch.money_spent_max_without_fee * 1.4;
        //         }

        //         batch.money_not_spent_without_fee = batch.count_assignments_rejected * batch.reward;
        //         if(batch.count_assignments_per_hit < 10) {
        //             batch.money_not_spent_with_fee = batch.money_not_spent_without_fee * 1.2;
        //         } else {
        //             batch.money_not_spent_with_fee = batch.money_not_spent_without_fee * 1.4;
        //         }
        //     });

        //     console.log(state.object_batches)

        //     state.object_batches = dict_batches;
        // },
        // setObjectBatches(state, dict_batches) {
        //     for(let id_batch in dict_batches) {
        //         state.object_batches[id_batch] = dict_batches[id_batch];
        //     };
        //     state.object_batches = dict_batches;
        // },
        set_batches(state, {data, use_sandbox}) {
            let array_batches = null;
            if(use_sandbox)
            {
                state.array_batches_sandbox = [];
                array_batches = state.array_batches_sandbox;
            } else {
                state.array_batches = [];
                array_batches = state.array_batches;
            }

            _.forEach(data, function(data_batch){
                const batch = new Batch(data_batch);
                Vue.set(array_batches, array_batches.length, batch);
                // Vue.set(object_batches, batch.id, batch);
            });
        },
        clear_batches_selected(state) {
            state.object_batches_selected = {};
        },
		set_batches_selected(state, {array_items, add}) {
            if(add === true) {
                _.forEach(array_items, (item) => {
                    Vue.set(state.object_batches_selected, item.id, item.id);
                })
            } else {
                _.forEach(array_items, (item) => {
                    Vue.delete(state.object_batches_selected, item.id);
                })
            }
		},
        // append_batches(state, {data_batches, use_sandbox}) {
        //     let object_batches = null;
        //     if(use_sandbox)
        //     {
        //         object_batches = state.object_batches_sandbox;
        //     } else {
        //         object_batches = state.object_batches;
        //     }

        //     _.forEach(data_batches, function(data_batch){
        //         const batch = new Batch(data_batch);
        //         Vue.set(object_batches, batch.id, batch);
        //     });
        // },
        add_workers(state, {object_workers, use_sandbox}) {
            // console.log('#####')
            let object_batches = null;
            if(use_sandbox)
            {
                object_batches = state.object_batches_sandbox;
            } else {
                object_batches = state.object_batches;
            }
            _.forEach(object_batches, function(batch){
                _.forEach(batch.object_hits, function(hit){
                    _.forEach(hit.object_assignments, function(assignment){
                        if(_.isObject(assignment.worker))
                        {
                            // skip if assignment has already worker
                            return true;
                        }
                        Vue.set(assignment, 'worker', object_workers[assignment.worker]);
                        // assignment.worker = object_workers[assignment.worker];
                        // Vue.set(assignment.worker, );
                    });
                });
            });
        },
        add_batch(state, {data_batch, use_sandbox}) {
            let object_batches = null;
            if(use_sandbox)
            {
                object_batches = state.object_batches_sandbox;
            } else {
                object_batches = state.object_batches;
            }

            const obj_batch = new Batch(data_batch);
            Vue.set(object_batches, obj_batch.id, obj_batch);

            // _.forEach(data_batch.hits, function(data_hit) {
            //     data_hit.batch = batch;
            //     const hit = new HIT(data_hit);

            //     Vue.set(object_hits, hit.id, hit);

            //     Vue.set(batch.hits, batch.hits.length, hit);
            // });
        },
        set_urls(state, config) {
            state.url_api_projects_batches = config.url_api_projects_batches;
            state.url_api_projects_batches_download = config.url_api_projects_batches_download;
            state.url_api_projects_batches_download_info = config.url_api_projects_batches_download_info;
        },
        set_csv_parsed(state, csv_parsed) {
            state.object_csv_parsed = csv_parsed;
        },
        set_is_syncing_mturk(state, value) {
            state.is_syncing_mturk = value;
        },
        clear_sandbox(state) {
            state.object_batches_sandbox = {}; 
        },
        reset: (state) => {
            state.object_batches = null;
            state.object_batches_sandbox = null;
            state.object_csv_parsed = undefined;
            state.is_syncing_mturk = false;
        }
	},
	actions: {
	},
}