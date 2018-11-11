import Vuex from 'vuex';
// import Vue from 'vue/dist/vue.common';
import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import _ from 'lodash';
import HIT from '../../classes/hit.js';

import VueCookies from 'vue-cookies'
Vue.use(Vuex)
Vue.use(VueCookies)
Vue.use(VueAxios, axios)

export const moduleHITs = {
	namespaced: true,
	state: {
        object_hits: {},
		object_hits_sandbox: {},
	},
    getters: {
        get_object_hits: (state, getters, rootState) => (use_sandbox=undefined) => {
            if(use_sandbox == undefined)
            {
                return rootState.use_sandbox ? state.object_hits_sandbox : state.object_hits;
            } else {
                return use_sandbox ? state.object_hits_sandbox : state.object_hits;
            }
        },
        list_hits: (state, getters) => {
            if(Object.keys(getters.get_object_hits()).length == 0)
            {
                return [];
            }
            return _.orderBy(getters.get_object_hits(), ['datetime_creation'], ['desc']);
        },
    },
	mutations: {
		set_hits(state, {object_batches, data_batches, use_sandbox}) {
            let object_hits = null;
            if(use_sandbox)
            {
                object_hits = state.object_hits_sandbox;
            } else {
                object_hits = state.object_hits;
            }

            _.forEach(data_batches, function(data_batch) {
            	const id_batch = data_batch.id;
            	const batch = object_batches[id_batch];

                _.forEach(data_batch.hits, function(data_hit) {
                	data_hit.batch = batch;
		            const hit = new HIT(data_hit);

		            Vue.set(object_hits, hit.id, hit);

		            Vue.set(batch.object_hits, hit.id, hit);
                });
            });
		},
        clear_sandbox(state) {
            state.object_hits_sandbox = {}; 
        },
        reset: (state) => {
            state.object_hits = {};
            state.object_hits_sandbox = {};
        }
	},
	actions: {
        async set_hits({commit, state, getters, rootState, rootGetters, dispatch}, {object_batches, data_batches, use_sandbox}) {           
            // console.log('set_hits');
            commit('set_hits', {
                object_batches, 
                data_batches, 
                use_sandbox
            });
            // console.log('after set_hits');

            // console.log('dispatch_set_assignments');
            await dispatch('moduleAssignments/set_assignments', {
                data_batches, 
                'object_hits': getters.get_object_hits(use_sandbox), 
                use_sandbox
            }, {root: true});
            // console.log('after dispatch_set_assignments');
        },
        async append_hits({commit, state, getters, rootState, rootGetters, dispatch}, {data_batches, use_sandbox}) {
            // commit('set_hits', {
            //     object_batches, 
            //     data_batches, 
            //     use_sandbox
            // });
            await dispatch('moduleAssignments/append_assignments', {
                // object_batches, 
                data_batches, 
                'object_hits': getters.get_object_hits(use_sandbox), 
                use_sandbox,
            }, {root: true});
        },
	},
}