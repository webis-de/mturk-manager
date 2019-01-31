import Vue from 'vue';
import _ from 'lodash';
import HIT from '../../classes/hit.js';

import Batch from "../../classes/batch";
import localforage from "localforage";

export const moduleHITs = {
	namespaced: true,
	state: {
        object_hits: {},
		object_hits_sandbox: {},

        array_hits: null,
        array_hits_sandbox: null,

        object_hits_selected: {},

        array_columns_general: [
            {
                text: 'ID',
                value: 'id_hit',
            },
            {
                text: 'Batch',
                value: 'batch',
            },
            {
                text: 'Creation',
                value: 'datetime_creation',
            },
            {
                text: 'Progress',
                value: 'progress',
                align: 'center',
                sortable: false,
            },
        ],
        array_columns_selected_initial_general: [
            'id_hit',
            'batch',
            'datetime_creation',
            'progress',
        ],
        array_columns_selected_general: null,

        url_api_projects_hits: undefined,
	},
    getters: {
	    get_array_columns_general: (state) => {
	        return state.array_columns_general;
        },
	    get_array_columns_selected_general: (state) => {
	        if(state.array_columns_selected_general === null) {
	            return state.array_columns_selected_initial_general;
            } else {
                return state.array_columns_selected_general;
            }
        },
	    get_array_columns_selected_initial_general: (state) => {
	        return state.array_columns_selected_initial_general;
        },

	    get_object_hits_selected: (state) => {
	        return state.object_hits_selected;
        },
        get_array_hits: (state, getters, rootState) => (use_sandbox=undefined) => {
            if(use_sandbox == undefined)
            {
                return rootState.module_app.use_sandbox ? state.array_hits_sandbox : state.array_hits;
            } else {
                return use_sandbox ? state.array_hits_sandbox : state.array_hits;
            }
        },
        get_array_hits_sandbox: (state) => {
            return state.array_hits_sandbox
        },
        get_object_hits: (state, getters, rootState) => (use_sandbox=undefined) => {
            if(use_sandbox == undefined)
            {
                return rootState.module_app.use_sandbox ? state.object_hits_sandbox : state.object_hits;
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
        set_array_columns_general(state, array_columns) {
            localforage.setItem('array_columns_hits_general', array_columns);
            state.array_columns_selected_general = array_columns;
        },

        set_hits(state, {data, use_sandbox}) {
            let array_hits = null;
            if(use_sandbox)
            {
                state.array_hits_sandbox = [];
                array_hits = state.array_hits_sandbox;
            } else {
                state.array_hits = [];
                array_hits = state.array_hits;
            }

            _.forEach(data, function(data){
                const hit = new HIT(data);
                Vue.set(array_hits, array_hits.length, hit);
            });
        },
        clear_hits_selected(state) {
            state.object_hits_selected = {};
        },
		set_hits_selected(state, {array_items, add}) {
            if(add === true) {
                _.forEach(array_items, (item) => {
                    Vue.set(state.object_hits_selected, item.id, item.id);
                })
            } else {
                _.forEach(array_items, (item) => {
                    Vue.delete(state.object_hits_selected, item.id);
                })
            }
		},
		// set_hits(state, {object_batches, data_batches, use_sandbox}) {
        //     let object_hits = null;
        //     if(use_sandbox)
        //     {
        //         object_hits = state.object_hits_sandbox;
        //     } else {
        //         object_hits = state.object_hits;
        //     }
        //
        //     _.forEach(data_batches, function(data_batch) {
        //     	const id_batch = data_batch.id;
        //     	const batch = object_batches[id_batch];
        //
        //         _.forEach(data_batch.hits, function(data_hit) {
        //         	data_hit.batch = batch;
		//             const hit = new HIT(data_hit);
        //
		//             Vue.set(object_hits, hit.id, hit);
        //
		//             Vue.set(batch.object_hits, hit.id, hit);
        //         });
        //     });
		// },
        clear_sandbox(state) {
            state.object_hits_sandbox = {}; 
        },
        reset: (state) => {
            state.object_hits = {};
            state.object_hits_sandbox = {};
        },
        set_urls(state, config) {
            state.url_api_projects_hits = config.url_api_projects_hits;
        },
	},
	actions: {
	    async init({state}) {
	        let array_columns = await localforage.getItem('array_columns_hits_general');
            if(array_columns !== null)
            {
                state.array_columns_selected_general = array_columns;
            } else {
                state.array_columns_selected_general = state.array_columns_selected_initial_general;
            }
        },
        reset_array_columns_general({state, commit}) {
	        commit('set_array_columns_general', state.array_columns_selected_initial_general);
        },
	},
}