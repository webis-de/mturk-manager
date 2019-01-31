import _ from 'lodash';
import Vue from 'vue';

export const moduleMessagesReject = {
	namespaced: true,
	state: {
        object_messages_reject: null,
        url_api_messages_reject: undefined,
	},
	getters: {
    	get_object_messages_reject: (state) => {
			return state.object_messages_reject;
    	},
    	get_list_messages_reject: (state) => {
			return _.orderBy(state.object_messages_reject, 'count_usage', 'desc');
    	},
	},
	mutations: {
		set_messages_reject(state, data) {
        	state.object_messages_reject= {};
        	
        	_.forEach(data, function(message_reject){
    			// const object_project = new Project(message_reject);
    			Vue.set(state.object_messages_reject, message_reject.message, message_reject);
        	});
		},
		add_message_reject(state, {message_reject}) {
			Vue.set(state.object_messages_reject, message_reject.message, message_reject);
		},
        set_urls(state, config) {
            state.url_api_messages_reject = config.url_api_messages_reject;
		},
	},
	actions: {
	},
}