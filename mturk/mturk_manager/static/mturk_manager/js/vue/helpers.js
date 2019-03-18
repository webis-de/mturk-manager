import localforage from 'localforage';
import _ from 'lodash';

// Saves the pagination information of a given table to vuex and localforage
export function setPagination({ pagination, setPageTo1, state, namePagination, nameLocalStorage }) {
  if (setPageTo1 === true) {
    // necessary to prevent duplicated requests
    state[namePagination].page = 1;
    localforage.setItem(nameLocalStorage, state[namePagination]);
    return;
  }

  const objectToBeStored = _.pick(pagination, ['page', 'rowsPerPage', 'sortBy', 'descending']);
  localforage.setItem(nameLocalStorage, objectToBeStored);
  state[namePagination] = objectToBeStored;
}

// loads the pagination information for a given table from localforage and saves it to vuex
export async function initPagination({ commit, nameLocalStorage, nameMutation }) {
  const objectPagination = await localforage.getItem(nameLocalStorage);

  if (objectPagination !== null) {
    commit(nameMutation, {
      pagination: objectPagination,
    });
  }
}

export function setState({ state, objectState, nameState, nameLocalStorage }) {
  const objectStateCloned = _.cloneDeep(objectState);

  if(nameLocalStorage !== undefined) {
    localforage.setItem(nameLocalStorage, objectStateCloned);
  }

  state[nameState] = objectStateCloned;
}

export async function initState({ commit, nameLocalStorage, nameState, objectStateDefault }) {
  const objectState = await localforage.getItem(nameLocalStorage);
  console.warn('nameLocalStorage', nameLocalStorage);
  console.warn('objectState', objectState);
  commit('setState', {
    objectState: objectState === null ? _.cloneDeep(objectStateDefault) : objectState,
    nameState,
    nameLocalStorage,
  });
}
