import _ from 'lodash';
import Vue from 'vue';

export const moduleKeywords = {
	namespaced: true,
	state: {
        object_keywords: null,
        url_api_keywords: undefined,
	},
	getters: {
    	get_object_keywords: (state) => {
			return state.object_keywords;
    	},
	},
	mutations: {
		set_keywords(state, data) {
        	state.object_keywords= {};
        	
        	_.forEach(data, function(keyword){
    			// const object_project = new Project(keyword);
    			Vue.set(state.object_keywords, keyword.text, keyword);
        	});
		},
        set_urls(state, config) {
            state.url_api_keywords = config.url_api_keywords;
		},
	},
	actions: {
	},
}