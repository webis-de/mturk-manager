import Vuex from 'vuex';
// import Vue from 'vue/dist/vue.common';
import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import _ from 'lodash';
import Batch from '../../classes/batch.js';
import HIT from '../../classes/hit.js';

import VueCookies from 'vue-cookies'
Vue.use(Vuex)
Vue.use(VueCookies)
Vue.use(VueAxios, axios)

export const moduleBatches = {
	namespaced: true,
	state: {
        object_batches: null,
		object_batches_sandbox: null,
        url_api_assignments_real_approved: undefined,

        url_api_projects_batches: undefined,

        object_csv_parsed: undefined,
	},
    getters: {
        get_object_batches: (state, getters, rootState) => (use_sandbox=undefined) => {
            if(use_sandbox == undefined)
            {
                return rootState.use_sandbox ? state.object_batches_sandbox : state.object_batches;
            } else {
                return use_sandbox ? state.object_batches_sandbox : state.object_batches;
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

        list_batches: (state, getters) => {
            if(getters.get_object_batches() == null)
            {
                return [];
            }
            return _.orderBy(getters.get_object_batches(), ['datetime_creation'], ['desc']);
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

            // console.log(state.object_batches_sandbox)

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
        // setObjectBatches(state, dict_batches) {
        //     for(let id_batch in dict_batches) {
        //         state.object_batches[id_batch] = dict_batches[id_batch];
        //     };
        //     state.object_batches = dict_batches;
        // },
        set_batches(state, {data_batches, use_sandbox}) {
            let object_batches = null;
            if(use_sandbox)
            {
                state.object_batches_sandbox = {};
                object_batches = state.object_batches_sandbox;
            } else {
                state.object_batches = {};
                object_batches = state.object_batches;
            }

            _.forEach(data_batches, function(data_batch){
                const batch = new Batch(data_batch);
                Vue.set(object_batches, batch.id, batch);
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
        },
        set_csv_parsed(state, csv_parsed) {
            state.object_csv_parsed = csv_parsed;
        },
	},
	actions: {
        async sync_mturk({commit, state, getters, rootState, rootGetters, dispatch}) {
            const use_sandbox = rootState.use_sandbox;

            await dispatch('make_request', {
                method: 'patch',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_batches,
                    use_sandbox, 
                }),
             }, { root: true }).then(response => {
                console.log(response);
                // commit('set_batches', {'data_batches': response.data, use_sandbox});

                // commit('add_settings_batch', {
                //     data: response.data,
                //     project: data.project,
                // });
            });
        },
        // async sync_database({commit, state, getters, rootState, rootGetters}, force=false) {
        //     if(getters.get_object_batches == null || force) {
        //         await axios.get(rootGetters.get_url_api(state.url_api_assignments_real_approved))
        //         .then(response => {
        //             if(rootState.use_sandbox) {
        //                 commit('setBatchesAndHits_sandbox', response.data);
        //             } else {
        //                 commit('setBatchesAndHits', response.data);
        //             }
        //         })
        //     }
        // },

        async sync_batches({commit, state, getters, rootState, rootGetters, dispatch}, force=false) {
            const use_sandbox = rootState.use_sandbox;

            if(getters.get_object_batches(use_sandbox) == null || force) {
                await dispatch('make_request', {
                    method: 'get',
                    url: rootGetters.get_url_api({
                        url: state.url_api_projects_batches, 
                    }),
                }, { root: true }).then(response => {
                    commit('set_batches', {
                        'data_batches': response.data, 
                        use_sandbox
                    });

                    commit('moduleHITs/set_hits', {
                        'object_batches': getters.get_object_batches(use_sandbox), 
                        'data_batches': response.data, 
                        use_sandbox
                    }, {root: true});

                    // commit('add_settings_batch', {
                    //     data: response.data,
                    //     project: data.project,
                    // });
                });

                // await axios.get(rootGetters.get_url_api(state.url_api_projects_batches, use_sandbox))
                // .then(response => {
                //     commit('set_batches', {'data_batches': response.data, use_sandbox});
                // })

                // await axios.get(rootGetters.get_url_api(state.url_api_global_db, use_sandbox))
                // .then(response => {
                //     commit('set_data_global_db', {'data': response.data, use_sandbox});
                // })
            }
        },
        async add_batch({state, commit, getters, rootState, rootGetters, dispatch}, data) {
            const use_sandbox = rootState.use_sandbox;
            console.log(use_sandbox);
            console.log(data);
            console.log(state.url_api_projects_batches)
            await dispatch('make_request', {
                method: 'post',
                url: rootGetters.get_url_api({
                    url: state.url_api_projects_batches, 
                }),
                data: data,
            }, { root: true }).then(response => {
                console.log(response)
                commit('add_batch', {
                    data_batch: response.data,
                    use_sandbox,
                });

                commit('moduleHITs/set_hits', {
                    'object_batches': getters.get_object_batches(use_sandbox), 
                    'data_batches': [response.data], 
                    use_sandbox
                }, {root: true});
            });

            return 
            // await axios.post(
            //     rootGetters.get_url_api(state.url_api_projects_batches, use_sandbox),
            //     JSON.stringify(data),
            //     {
            //         headers: {
            //             "X-CSRFToken": rootState.token_csrf,
            //             "Content-Type": 'application/json',
            //         }
            //     },
            // )
            // .then(response => {
            //     commit('add_batch', {'data_batch': response.data, use_sandbox});
            // })
        },
	},
}