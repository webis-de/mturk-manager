import _ from 'lodash';
import localforage from 'localforage';
import Vue from 'vue';

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
    updateState(state, { objectStateCurrent, objectStateNew, fields }) {
      _.forEach(fields, (nameField) => {
        Vue.set(objectStateCurrent, nameField, _.cloneDeep(objectStateNew[nameField]));
      });
    },
  },
  actions: {
    async loadState({ commit }, { nameState, nameLocalStorage, objectStateDefault = null }) {
      const objectState = await localforage.getItem(nameLocalStorage);

      if (objectState === null) {
        if (objectStateDefault !== null) {
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
      // console.warn('objectState', objectState);
      // console.warn('nameState', nameState);
      // console.warn('nameLocalStorage', nameLocalStorage);
      commit('setState', {
        objectState,
        nameState,
      });

      if (nameLocalStorage !== undefined) {
        await localforage.setItem(nameLocalStorage, objectState);
      }
    },
    async updateState({ commit }, { objectStateCurrent, objectStateNew, fields, nameLocalStorage }) {
      commit('updateState', {
        objectStateCurrent,
        objectStateNew,
        fields,
      });

      if (nameLocalStorage !== undefined) {
        await localforage.setItem(nameLocalStorage, objectStateCurrent);
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
