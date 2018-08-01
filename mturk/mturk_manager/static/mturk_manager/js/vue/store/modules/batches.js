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

export const moduleBatches= {
	namespaced: true,
	state: {
        object_batches: null,
		object_batches_sandbox: null,
        url_api_assignments_real_approved: undefined,
	},
    getters: {
        get_object_batches: (state, getters, rootState) => {
            return rootState.use_sandbox ? state.object_batches_sandbox : state.object_batches;
        },
        list_batches: (state, getters) => {
            if(getters.get_object_batches == null)
            {
                return [];
                // return {};
            }

            return _.orderBy(getters.get_object_batches, ['datetime_creation'], ['desc']);
        },
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
    },
	mutations: {
        setBatchesAndHits_sandbox(state, {list_hits, dict_batches}) {
            // set batches
            state.object_batches_sandbox = {};
            _.forIn(dict_batches, function(batch, id_batch) {
                state.object_batches_sandbox[id_batch] = batch;
                state.object_batches_sandbox[id_batch]['hits'] = [];

            });

            // set hits
            _.forEach(list_hits, function(hit){
                // console.log(Date.parse(hit.datetime_creation));
                hit.datetime_creation = new Date(hit.datetime_creation);

                state.object_batches_sandbox[hit.id_batch].hits.push(hit);
            });


            _.forIn(state.object_batches_sandbox, function(batch, id_batch) {
                // datetime of last hit is created time of batch
                batch.datetime_creation = batch.hits[0].datetime_creation;

                batch.count_assignments_approved = _.sumBy(
                    batch.hits, 'count_assignments_approved'
                );
                batch.count_assignments_rejected = _.sumBy(
                    batch.hits, 'count_assignments_rejected'
                );

                batch.count_assignments_total =  batch.hits.length * batch.count_assignments_per_hit;

                batch.money_spent_without_fee = batch.count_assignments_approved * batch.reward;
                if(batch.count_assignments_per_hit < 10) {
                    batch.money_spent_with_fee = batch.money_spent_without_fee * 1.2;
                } else {
                    batch.money_spent_with_fee = batch.money_spent_without_fee * 1.4;
                }

                batch.money_spent_max_without_fee = batch.count_assignments_total * batch.reward;
                if(batch.count_assignments_per_hit < 10) {
                    batch.money_spent_max_with_fee = batch.money_spent_max_without_fee * 1.2;
                } else {
                    batch.money_spent_max_with_fee = batch.money_spent_max_without_fee * 1.4;
                }

                batch.money_not_spent_without_fee = batch.count_assignments_rejected * batch.reward;
                if(batch.count_assignments_per_hit < 10) {
                    batch.money_not_spent_with_fee = batch.money_not_spent_without_fee * 1.2;
                } else {
                    batch.money_not_spent_with_fee = batch.money_not_spent_without_fee * 1.4;
                }
            });

            console.log(state.object_batches_sandbox)

            state.object_batches_sandbox = dict_batches;
        },
        setBatchesAndHits(state, {list_hits, dict_batches}) {
            // set batches
            state.object_batches = {};
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

                batch.count_assignments_approved = _.sumBy(
                    batch.hits, 'count_assignments_approved'
                );
                batch.count_assignments_rejected = _.sumBy(
                    batch.hits, 'count_assignments_rejected'
                );

                batch.count_assignments_total =  batch.hits.length * batch.count_assignments_per_hit;

                batch.money_spent_without_fee = batch.count_assignments_approved * batch.reward;
                if(batch.count_assignments_per_hit < 10) {
                    batch.money_spent_with_fee = batch.money_spent_without_fee * 1.2;
                } else {
                    batch.money_spent_with_fee = batch.money_spent_without_fee * 1.4;
                }

                batch.money_spent_max_without_fee = batch.count_assignments_total * batch.reward;
                if(batch.count_assignments_per_hit < 10) {
                    batch.money_spent_max_with_fee = batch.money_spent_max_without_fee * 1.2;
                } else {
                    batch.money_spent_max_with_fee = batch.money_spent_max_without_fee * 1.4;
                }

                batch.money_not_spent_without_fee = batch.count_assignments_rejected * batch.reward;
                if(batch.count_assignments_per_hit < 10) {
                    batch.money_not_spent_with_fee = batch.money_not_spent_without_fee * 1.2;
                } else {
                    batch.money_not_spent_with_fee = batch.money_not_spent_without_fee * 1.4;
                }
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
        set_url_api_assignments_real_approved(state, url_new) {
            state.url_api_assignments_real_approved = url_new;
        },
	},
	actions: {
        async sync_database({commit, state, getters, rootState, rootGetters}, force=false) {
            if(getters.get_object_batches == null || force) {
                await axios.get(rootGetters.get_url_api(state.url_api_assignments_real_approved))
                .then(response => {
                    if(rootState.use_sandbox) {
                        commit('setBatchesAndHits_sandbox', response.data);
                    } else {
                        commit('setBatchesAndHits', response.data);
                    }
                })
            }
        },
	},
}