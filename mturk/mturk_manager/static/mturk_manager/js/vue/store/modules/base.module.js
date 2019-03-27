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

      if(objectState === null) {
        if(objectStateDefault !== null) {
          commit('setState', {
            objectState: objectStateDefault,
            nameState,
          });
        }
      } else {
        commit('setState', {
          objectState,
          nameState,
        });
      }
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
// // loads the pagination information for a given table from localforage and saves it to vuex
// export async function initPagination({ commit, nameLocalStorage, nameMutation }) {
//   const objectPagination = await localforage.getItem(nameLocalStorage);
//
//   if (objectPagination !== null) {
//     commit(nameMutation, {
//       pagination: objectPagination,
//     });
//   }
// }