import axios from 'axios';
import { setState } from '../../helpers';

export const module_finances = {
  namespaced: true,
  state: {
    balance: null,
    balance_sandbox: null,
    url_api_projects_balance: undefined,
    url_api_projects_finances: undefined,

    sum_costs_max: null,
    sum_costs_so_far: null,
  },
  getters: {
    get_balance: (state, getters, rootState) => (use_sandbox = undefined) => {
      if (use_sandbox === undefined) {
        return rootState.module_app.use_sandbox
          ? state.balance_sandbox
          : state.balance;
      }
      return use_sandbox ? state.balance_sandbox : state.balance;
    },
  },
  mutations: {
    setState(state, { objectState, nameState, nameLocalStorage }) {
      setState({
        state,
        objectState,
        nameState,
        nameLocalStorage,
      });
    },
    set_balance(state, balance_new) {
      state.balance = balance_new;
    },
    set_balance_sandbox(state, balance_new) {
      state.balance_sandbox = balance_new;
    },
    set_urls(state, config) {
      state.url_api_projects_balance = config.url_api_projects_balance;
      state.url_api_projects_finances = config.url_api_projects_finances;
    },
  },
};
