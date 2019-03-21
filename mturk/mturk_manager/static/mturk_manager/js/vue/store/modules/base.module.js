import {setState} from '../../helpers';
import _ from 'lodash';
import localforage from "localforage";

export default {
  namespaced: true,
  state: {
  },
  getters: {
  },
  mutations: {
    setState(state, { objectState, nameState }) {
      state[nameState] = _.cloneDeep(objectState);
    },
  },
  actions: {
    async loadState({ commit }, { nameState, nameLocalStorage, objectStateDefault = null }) {
      const objectState = await localforage.getItem(nameLocalStorage);

      commit('setState', {
        objectState: objectState === null ? _.cloneDeep(objectStateDefault) : objectState,
        nameState,
      });
    },
    async setState({ commit }, { objectState, nameState, nameLocalStorage }) {
      commit('setState', {
        objectState,
        nameState,
      });

      if(nameLocalStorage !== undefined) {
        await localforage.setItem(nameLocalStorage, objectState);
      }
    },
  },
};