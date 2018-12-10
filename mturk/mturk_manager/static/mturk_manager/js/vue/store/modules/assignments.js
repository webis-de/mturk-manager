import Vuex from 'vuex';
// import Vue from 'vue/dist/vue.common';
import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import _ from 'lodash';
import Assignment from '../../classes/assignment.js';

import VueCookies from 'vue-cookies'
import HIT from "../../classes/hit";
Vue.use(Vuex)
Vue.use(VueCookies)
Vue.use(VueAxios, axios)

export const moduleAssignments = {
	namespaced: true,
	state: {
        object_assignments: {},
		object_assignments_sandbox: {},

        array_assignments: null,
        array_assignments_sandbox: null,
        url_api_projects_assignments: undefined,

		set_ids_worker: null,
		object_assignments_selected: {},
	},
    getters: {
	    get_array_assignments_selected: (state) => {
	        return _.orderBy(state.object_assignments_selected)
        },
	    get_object_assignments_selected: (state) => {
	        return state.object_assignments_selected
        },
        get_array_assignments: (state) => {
            return state.array_assignments
        },
        get_array_assignments_sandbox: (state) => {
            return state.array_assignments_sandbox
        },
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
        set_ids_worker: (state) => {
            return state.set_ids_worker;
        },
    },
	mutations: {
        set_assignments(state, {data, use_sandbox}) {
            let array_assignments = null;
            if(use_sandbox)
            {
                state.array_assignments_sandbox = [];
                array_assignments = state.array_assignments_sandbox;
            } else {
                state.array_assignments = [];
                array_assignments = state.array_assignments;
            }

            _.forEach(data, function(data){
                const assignment = new Assignment(data);
                Vue.set(array_assignments, array_assignments.length, assignment);
            });
        },
		// set_assignments(state, {data_assignments, object_hits, use_sandbox}) {
        //     let object_assignments = null;
        //     if(use_sandbox)
        //     {
        //         object_assignments = state.object_assignments_sandbox;
        //     } else {
        //         object_assignments = state.object_assignments;
        //     }
        //     // console.log('########')
        //     state.set_ids_worker = new Set();
        //
        //     _.forEach(data_batches, function(data_batch) {
        //         _.forEach(data_batch.hits, function(data_hit) {
	    //         	const id_hit = data_hit.id;
	    //         	const hit = object_hits[id_hit];
        //
        //
	    //             _.forEach(data_hit.assignments, function(data_assignment) {
	    //             	state.set_ids_worker.add(data_assignment.worker);
	    //             	data_assignment.hit = hit;
	    //             	// console.log(hit)
		// 	            const assignment = new Assignment(data_assignment);
	    //             	// console.log(assignment)
        //
		// 	            Vue.set(object_assignments, assignment.id, assignment);
        //
		// 	            Vue.set(hit.object_assignments, assignment.id, assignment);
		//             });
        //         });
        //     });
        //     // console.log('########')
        //
        //     // console.log(state.set_ids_worker);
		// },
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
        clear_assignments_selected(state) {
            state.object_assignments_selected = {};
        },
		set_assignments_selected(state, {array_items, add}) {
            if(add === true) {
                _.forEach(array_items, (item) => {
                    Vue.set(state.object_assignments_selected, item.id, item.id);
                })
            } else {
                _.forEach(array_items, (item) => {
                    Vue.delete(state.object_assignments_selected, item.id);
                })
            }
		},
        reset: (state) => {
            state.object_assignments = {};
            state.object_assignments_sandbox = {};
            state.set_ids_worker = null;
            state.object_assignments_selected = {};
        },
        set_urls(state, config) {
            state.url_api_projects_assignments = config.url_api_projects_assignments;
        },
	},
	actions: {
	},
}