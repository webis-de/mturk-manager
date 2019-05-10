import axios from 'axios';
import { setState } from '../../helpers';
import _ from 'lodash';
import baseModule from './base.module';

export const module_finances = _.merge({}, baseModule, {
  namespaced: true,
  state: {
    balance: null,
    balance_sandbox: null,
    url_api_projects_balance: undefined,
    url_api_projects_finances: undefined,

    // sum_costs_max: null,
    // sum_costs_so_far: null,
    // sum_costs_pending: null,
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
    set_balance(state, balance_new) {
      state.balance = parseInt(parseFloat(balance_new) * 100, 10);
    },
    set_balance_sandbox(state, balance_new) {
      state.balance_sandbox = parseInt(parseFloat(balance_new) * 100, 10);;
    },
    set_urls(state, config) {
      state.url_api_projects_balance = config.url_api_projects_balance;
      state.url_api_projects_finances = config.url_api_projects_finances;
    },
  },
});
