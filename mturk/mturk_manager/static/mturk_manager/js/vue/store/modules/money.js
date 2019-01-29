import axios from 'axios';

export const moduleMoney = {
	namespaced: true,
	state: {
		balance: null,
		balance_sandbox: null,
        url_api_get_balance: undefined,
	},
	getters: {
    	get_balance: (state, getters, rootState) => {
    		return rootState.module_app.use_sandbox ? state.balance_sandbox : state.balance;
    	},
	},
	mutations: {
		set_balance(state, balance_new) {
			state.balance = balance_new;
		},
		set_balance_sandbox(state, balance_new) {
			state.balance_sandbox = balance_new;
		},
        setUrlApiGetBalance(state, url_new) {
            state.url_api_get_balance = url_new;
        },
	},
	actions: {
		async update_balance({commit, state, rootState, rootGetters}, force) {
            if(state.balance == null || force) {
				await axios.get(rootGetters.get_url_api(state.url_api_get_balance))
			    .then(response => {
			    	if(rootState.module_app.use_sandbox) {
	                	commit('set_balance_sandbox', response.data.balance);
			    	} else {
	                	commit('set_balance', response.data.balance);
			    	}
			    })
			}
		},
	},
}