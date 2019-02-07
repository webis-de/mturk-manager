import axios from 'axios';

export const module_finances = {
	namespaced: true,
	state: {
		balance: null,
		balance_sandbox: null,
        url_api_projects_balance: undefined,
	},
	getters: {
    	get_balance: (state, getters, rootState) => (use_sandbox=undefined) => {
            if(use_sandbox === undefined)
            {
            	return rootState.module_app.use_sandbox ? state.balance_sandbox : state.balance;
            } else {
                return use_sandbox ? state.balance_sandbox : state.balance;
            }
        },
	},
	mutations: {
		set_balance(state, balance_new) {
			state.balance = balance_new;
		},
		set_balance_sandbox(state, balance_new) {
			state.balance_sandbox = balance_new;
		},
        set_urls(state, config) {
            state.url_api_projects_balance = config.url_api_projects_balance;
        },
	},
}