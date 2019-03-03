import localforage from 'localforage';
import _ from 'lodash';

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

export async function initPagination({ commit, nameLocalStorage, nameMutation }) {
  const objectPagination = await localforage.getItem(nameLocalStorage);

  if (objectPagination !== null) {
    commit(nameMutation, {
      pagination: objectPagination,
    });
  }
}
