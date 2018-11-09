import Vuex from 'vuex';
// import Vue from 'vue/dist/vue.common';
import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import _ from 'lodash';
import Assignment from '../../classes/assignment.js';

import VueCookies from 'vue-cookies'
Vue.use(Vuex)
Vue.use(VueCookies)
Vue.use(VueAxios, axios)

export const moduleAssignments = {
	namespaced: true,
	state: {
        object_assignments: {},
		object_assignments_sandbox: {},
		set_ids_worker: null,
		assignments_selected: [],
	},
    getters: {
        get_object_assignments: (state, getters, rootState) => (use_sandbox=undefined) => {
            if(use_sandbox == undefined)
            {
                return rootState.use_sandbox ? state.object_assignments_sandbox : state.object_assignments;
            } else {
                return use_sandbox ? state.object_assignments_sandbox : state.object_assignments;
            }
        },
        list_assignments: (state, getters) => {
            if(Object.keys(getters.get_object_assignments()).length == 0)
            {
                return [];
            }
            return _.orderBy(getters.get_object_assignments(), ['datetime_creation'], ['desc']);
        },
    },
	mutations: {
		set_assignments(state, {data_batches, object_hits, use_sandbox}) {
            let object_assignments = null;
            if(use_sandbox)
            {
                object_assignments = state.object_assignments_sandbox;
            } else {
                object_assignments = state.object_assignments;
            }
            // console.log('########')
            state.set_ids_worker = new Set(); 

            _.forEach(data_batches, function(data_batch) {
                _.forEach(data_batch.hits, function(data_hit) {
	            	const id_hit = data_hit.id;
	            	const hit = object_hits[id_hit];


	                _.forEach(data_hit.assignments, function(data_assignment) {
	                	state.set_ids_worker.add(data_assignment.worker);
	                	data_assignment.hit = hit;
	                	// console.log(hit)
			            const assignment = new Assignment(data_assignment);
	                	// console.log(assignment)

			            Vue.set(object_assignments, assignment.id, assignment);

			            Vue.set(hit.object_assignments, assignment.id, assignment);
		            });
                });
            });
            // console.log('########')

            // console.log(state.set_ids_worker);
		},
        clear_sandbox(state) {
            state.object_assignments_sandbox = {}; 
        },
		// append_assignments(state, {object_batches, data_batches, object_hits, use_sandbox}) {
  //           let object_assignments = null;
  //           if(use_sandbox)
  //           {
  //               object_assignments = state.object_assignments_sandbox;
  //           } else {
  //               object_assignments = state.object_assignments;
  //           }

  //           state.set_ids_worker = new Set(); 

  //           _.forEach(data_batches, function(data_batch) {
  //           	const id_batch = data_batch.id;
  //           	const batch = object_batches[id_batch];

  //               _.forEach(data_batch.hits, function(data_hit) {
	 //            	const id_hit = data_hit.id;
	 //            	const hit = object_hits[id_hit];


	 //                _.forEach(data_hit.assignments, function(data_assignment) {
	 //                	state.set_ids_worker.add(data_assignment.worker);
	 //                	data_assignment.hit = hit;
		// 	            const assignment = new Assignment(data_assignment);

		// 	            Vue.set(object_assignments, assignment.id, assignment);

		// 	            Vue.set(hit.assignments, hit.assignments.length, assignment);
		//             });
  //               });
  //           });

  //           console.log(state.set_ids_worker);
		// },
		set_assignments_selected(state, assignments_selected) {
			state.assignments_selected = assignments_selected;
		},
	},
	actions: {
        async set_assignments({commit, state, getters, rootState, rootGetters, dispatch}, {data_batches, object_hits, use_sandbox}) {
            // console.log('set_assignments');
            commit('set_assignments', {
                data_batches, 
                object_hits,
                use_sandbox,
            });
            // console.log('after set_assignments');

            // console.log('dispatch_sync_workers_by_ids');
            await dispatch('moduleWorkers/sync_workers_by_ids', {
                list_ids: state.set_ids_worker,
                use_sandbox,
            }, {root: true});
            // console.log('after dispatch_sync_workers_by_ids');

        },
        async append_assignments({commit, state, getters, rootState, rootGetters, dispatch}, {data_batches, object_hits, use_sandbox}) {
            commit('set_assignments', {
                data_batches, 
                object_hits,
                use_sandbox,
            });

            dispatch('moduleWorkers/sync_workers_by_ids', {
                list_ids: state.set_ids_worker,
                use_sandbox,
                append: true,
            }, {root: true});

        },
	},
}