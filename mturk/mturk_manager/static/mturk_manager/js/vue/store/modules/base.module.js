import {setState} from '../../helpers';

export default {
  namespaced: true,
  state: {
  },
  getters: {
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
  },
  actions: {
  },
};