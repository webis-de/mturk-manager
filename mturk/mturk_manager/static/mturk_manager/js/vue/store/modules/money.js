import axios from 'axios';

export const moduleMoney = {
	namespaced: true,
	state: {
		balance: null,
        url_api_get_balance: undefined,
	},
	mutations: {
		setBalance(state, balance_new) {
			state.balance = balance_new;
		},
        setUrlApiGetBalance(state, url_new) {
            state.url_api_get_balance = url_new;
        },
	},
	actions: {
		async update_balance({commit, state}, force) {
            if(state.balance == null || force) {
				await axios.get(state.url_api_get_balance)
			    .then(response => {
			      commit('setBalance', response.data.balance);
			    })
			}
		},
	},
}