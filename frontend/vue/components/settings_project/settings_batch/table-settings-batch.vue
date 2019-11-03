<template>
  <div>
    <base-table
      title="Batch profiles"

      name-vuex-module="moduleSettingsBatch"
      name-state-pagination="paginationGeneral"
      name-local-storage-pagination="pagination_settings_batch_general"

      v-bind:function-load-page="loadPage"
      v-bind:array-items="arrayItems"

      name-state-columns="arrayColumns"
      name-state-columns-selected="objectColumnsSelectedInitialGeneral"

      v-bind:show-select="false"
    >
      <template
        v-slot:default="{ item, isCondensed }"
      >
        <item-settings-batch
          v-bind:item="item"
          v-bind:is-condensed="isCondensed"

          v-on:edited="snackbarEdited = true"
          v-on:deleted="snackbarDeleted = true"
        />
      </template>

      <template v-slot:actions>
        <component-add-settings-batch
          v-on:created="snackbarCreated = true"
        />
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
      v-model="snackbarCreated"
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
import { mapGetters, mapMutations, mapState } from 'vuex';
import ComponentAddSettingsBatch from './component_add_settings_batch';
import BaseTable from '../../base-table';
import { ServiceSettingsBatch } from '../../../services/service_settings_batch';
import ItemSettingsBatch from './item-settings-batch';

export default {
  name: 'TableSettingsBatch',
  components: {
    ItemSettingsBatch,
    BaseTable,
    ComponentAddSettingsBatch,
  },
  data() {
    return {
      loadPage: ServiceSettingsBatch.loadPage,

      snackbarDeleted: false,
      snackbarEdited: false,
      snackbarCreated: false,
    };
  },
  computed: {
    arrayItems() {
      const { arrayItems } = this.$store.state.moduleSettingsBatch;

      return arrayItems === null ? [] : arrayItems;
    },
    ...mapState('moduleSettingsBatch', ['arrayColumns']),
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
};
</script>
