<template>
  <div>
    <base-table
      v-bind:array-items="arrayItems"
      v-bind:array-columns="arrayColumns"
      v-bind:array-columns-selected="['name', 'actions']"
      v-bind:function-load-page="function_load_page"
      v-bind:is-condensed="false"

      v-bind:pagination-computed="paginationComputed"
      v-bind:function-set-pagination="functionSetPagination"
    >
      <template
        v-slot:default="{ props, array_columns_selected, isCondensed }"
      >
        <item-settings-batch
          v-bind:props="props"
          v-bind:is-condensed="isCondensed"

          v-on:edited="snackbarEdited = true"
          v-on:deleted="snackbarDeleted = true"
        />
      </template>

      <template v-slot:footer>
        <td colspan="2">
          <component-add-settings-batch
            v-on:created="snackbar_created = true"
          />
        </td>
      </template>
    </base-table>


    <!--<v+-->

    <v-snackbar
      v-model="snackbarDeleted"
      v-bind:timeout="1500"
      bottom
    >
      <v-spacer />
      Deleted!
      <v-spacer />
    </v-snackbar>

    <v-snackbar
      v-model="snackbar_created"
      v-bind:timeout="1500"
      bottom
      color="success"
    >
      <v-spacer />
      Saved!
      <v-spacer />
    </v-snackbar>

    <v-snackbar
      v-model="snackbarEdited"
      v-bind:timeout="1500"
      bottom
      color="success"
    >
      <v-spacer />
      Updated!
      <v-spacer />
    </v-snackbar>
  </div>
</template>

<script>
  import {mapGetters, mapMutations, mapState} from 'vuex';
import ComponentAddSettingsBatch from './component_add_settings_batch';
import { table } from '../../../mixins/table';
import BaseTable from '../../base-table';
import { ServiceSettingsBatch } from '../../../services/service_settings_batch';
import ItemSettingsBatch from './item-settings-batch';

export default {
  name: 'ComponentListSettingsBatch',
  components: {
    ItemSettingsBatch,
    BaseTable,
    ComponentAddSettingsBatch,
  },
  mixins: [table],
  data() {
    return {
      function_load_page: ServiceSettingsBatch.loadPage,

      snackbarDeleted: false,
      snackbarEdited: false,
      snackbar_created: false,
    };
  },
  computed: {
    ...mapState('moduleSettingsBatch', ['arrayColumns']),
    ...mapGetters('moduleSettingsBatch', ['arrayItems']),
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
    ...mapState('moduleSettingsBatch', {
      paginationComputed: 'paginationGeneral',
    }),
  },
  methods: {
    ...mapMutations('moduleSettingsBatch', {
      functionSetPagination: 'setPaginationGeneral',
    }),
  },
};
</script>
