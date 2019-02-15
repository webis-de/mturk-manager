import axios from 'axios';
import Vue from 'vue';
import _ from 'lodash';
import { Qualification } from '../../classes/qualifications.js';

export const moduleQualifications = {
  namespaced: true,
  state: {
    url_api_qualifications: undefined,
    // url_api_qualification: undefined,
    object_policies: null,
    object_policies_sandbox: null,
  },
  getters: {
    list_policies: (state, getters, rootState) => {
      const object_current = rootState.module_app.use_sandbox
        ? state.object_policies_sandbox
        : state.object_policies;

      if (object_current == null) {
        return [];
      }
      return _.orderBy(object_current, ['created_at'], ['desc']);
    },
  },
  mutations: {
    set_url_api_qualifications(state, url_new) {
      state.url_api_qualifications = url_new;
    },
    // set_url_api_qualification(state, url_new) {
    //     state.url_api_qualification = url_new;
    // },
    set_qualificiations(state, data_policies) {
      state.object_policies = {};
      _.forEach(data_policies, (data_policy) => {
        const obj_policy = new Qualification(data_policy);
        Vue.set(state.object_policies, obj_policy.id_mturk, obj_policy);
      });
    },
    set_qualificiations_sandbox(state, data_policies) {
      state.object_policies_sandbox = {};
      _.forEach(data_policies, (data_policy) => {
        const obj_policy = new Qualification(data_policy);
        Vue.set(state.object_policies_sandbox, obj_policy.id_mturk, obj_policy);
      });
    },
    add_qualification(state, obj_policy) {
      Vue.set(state.object_policies, obj_policy.id_mturk, obj_policy);
    },
    add_qualification_sandbox(state, obj_policy) {
      Vue.set(state.object_policies_sandbox, obj_policy.id_mturk, obj_policy);
    },
    delete_qualifications(state, list_ids) {
      _.forEach(list_ids, id => Vue.delete(state.object_policies, id));
    },
    delete_qualifications_sandbox(state, list_ids) {
      _.forEach(list_ids, id => Vue.delete(state.object_policies_sandbox, id));
    },
    // delete_qualifications(state, obj_policy) {
    // 	Vue.set(state.object_policies, obj_policy.id, obj_policy);
    // },
  },
  actions: {
    async sync_qualifications(
      {
        commit, state, rootGetters, rootState,
      },
      force = false,
    ) {
      const object_current = rootState.module_app.use_sandbox
        ? state.object_policies_sandbox
        : state.object_policies;

      if (object_current == null || force) {
        await axios
          .get(rootGetters.get_url_api(state.url_api_qualifications))
          .then((response) => {
            if (rootState.module_app.use_sandbox) {
              commit('set_qualificiations_sandbox', response.data);
            } else {
              commit('set_qualificiations', response.data);
            }
          });
      }
    },
    async update_qualification(
      {
        commit, state, rootGetters, rootState,
      },
      object_qualification,
    ) {
      await axios
        .put(
          rootGetters.get_url_api(
            state.url_api_qualifications,
            object_qualification.id_mturk,
          ),
          object_qualification.get_as_formdata(true),
          {
            headers: { 'X-CSRFToken': rootState.token_csrf },
          },
        )
        .then((response) => {
          if (rootState.module_app.use_sandbox) {
            commit(
              'add_qualification_sandbox',
              new Qualification(response.data),
            );
          } else {
            commit('add_qualification', new Qualification(response.data));
          }
        });
    },
    async add_qualification(
      {
        commit, state, rootGetters, rootState,
      },
      object_qualification,
    ) {
      await axios
        .post(
          rootGetters.get_url_api(state.url_api_qualifications),
          object_qualification.get_as_formdata(),
          {
            headers: { 'X-CSRFToken': rootState.token_csrf },
          },
        )
        .then((response) => {
          if (rootState.module_app.use_sandbox) {
            commit(
              'add_qualification_sandbox',
              new Qualification(response.data),
            );
          } else {
            commit('add_qualification', new Qualification(response.data));
          }
        });
    },
    async delete_qualifications(
      {
        commit, state, rootGetters, rootState,
      },
      list_qualifications,
    ) {
      const list_ids = list_qualifications.map(
        qualifiction => qualifiction.id_mturk,
      );

      const string_parameter = list_ids.map(id => `ids=${id}`).join('&');

      await axios
        .delete(
          rootGetters.get_url_api(state.url_api_qualifications)
            + string_parameter,
          {
            headers: {
              'X-CSRFToken': rootState.token_csrf,
            },
          },
        )
        .then((response) => {
          if (rootState.module_app.use_sandbox) {
            commit('delete_qualifications_sandbox', list_ids);
          } else {
            commit('delete_qualifications', list_ids);
          }
          // commit('add_qualification', new Qualification(response.data));
        });
    },
  },
};
