<template>
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
      v-slot:default="{ item, isCondensed, classes }"
    >
      <item-settings-batch
        v-bind:item="item"
        v-bind:is-condensed="isCondensed"
        v-bind:classes="classes"

        v-on:edited="snackbarEdited = true"
        v-on:deleted="snackbarDeleted = true"
      />
    </template>

    <template v-slot:actions="{ refresh }">
      <component-add-settings-batch
        v-on:created="refresh()"
      />
    </template>
  </base-table>
</template>

<script>
import { mapGetters, mapMutations, mapState } from 'vuex';
import ComponentAddSettingsBatch from './component_add_settings_batch';
import BaseTable from '../../base-table';
import { ServiceSettingsBatch } from '../../../services/settings-batch.service';
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
