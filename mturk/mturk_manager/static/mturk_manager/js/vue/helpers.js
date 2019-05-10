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

export function compareVersions(version1, version2) {
  if (version1 === version2) {
    return 0;
  }

  const version1Splitted = version1.split('.');
  const version2Splitted = version2.split('.');

  for (let i = 0; i < version1Splitted.length; i += 1) {
    if (version1Splitted[i] !== version2Splitted[i]) {
      if (parseInt(version1Splitted[i], 10) < parseInt(version2Splitted[i], 10)) {
        return -1;
      }

      return 1;
    }
  }

  return 0;
}

export function getChanges(item1, item2) {
  const object = {};

  // console.warn('item1', JSON.stringify(item1));
  // console.warn('item2', JSON.stringify(item2));

  for (const key in item2) {
    if (Object.prototype.hasOwnProperty.call(item2, key)) {
      if (item2[key] !== item1[key]) {
        if (typeof item1[key] === 'object' && item1[key] !== null && typeof item2[key] === 'object' && item2[key] !== null) {
          if (
            _.differenceBy(item1[key], item2[key], value => value.text.toLowerCase()).length > 0
            || _.differenceBy(item2[key], item1[key], value => value.text.toLowerCase()).length > 0
          ) {
            object[key] = item1[key];
          }
        } else {
          const value = item1[key];
          if (value === undefined) {
            object[key] = null;
          } else {
            object[key] = value;
          }
        }
      }
    }
  }

  return object;
}