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
