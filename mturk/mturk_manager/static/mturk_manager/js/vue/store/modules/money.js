import axios from 'axios';

export const moduleMoney = {
	namespaced: true,
	state: {
		balance: undefined,
	}, 
	mutations: {
		setBalance(state, balance_new) {
			state.balance = balance_new;
		},
	},
	actions: {
		async update_balance({commit, rootState}) {
			await axios.get(rootState.url_api_get_balance)
		    .then(response => {
		      commit('setBalance', response.data.balance);
		    })
		},
	},
}