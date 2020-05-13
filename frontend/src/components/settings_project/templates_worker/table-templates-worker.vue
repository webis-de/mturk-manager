<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div>
    <base-table
      title="Worker templates"

      name-vuex-module="moduleTemplates"
      name-state-pagination="paginationWorker"
      name-local-storage-pagination="pagination_templates_worker"

      v-bind:array-items="$store.getters['moduleTemplates/templatesWorker']"

      name-state-columns="arrayColumnsWorker"
      name-state-columns-selected="objectColumnsSelectedInitialGeneral"

      v-bind:show-select="false"
    >
      <template
        v-slot:default="{ item, objectColumnsSelected, isCondensed }"
      >
        <item-templates-worker
          v-bind:item="item"
          v-bind:object-columns-selected="objectColumnsSelected"
          v-bind:is-condensed="isCondensed"

          v-on:edited="snackbarEdited = true"
          v-on:deleted="snackbarDeleted = true"
        />
      </template>

      <template v-slot:actions>
        <component-add-template-worker
          v-on:created="snackbarCreated = true"
        />
      </template>
    </base-table>

    <v-snackbar
      v-model="snackbarDeleted"
      v-bind:timeout="1500"
      color="info"
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
      color="info"
    >
      <v-spacer />
      Saved!
      <v-spacer />
    </v-snackbar>

    <v-snackbar
      v-model="snackbarEdited"
      v-bind:timeout="1500"
      bottom
      color="info"
    >
      <v-spacer />
      Updated!
      <v-spacer />
    </v-snackbar>
  </div>
</template>

<script>
import { mapMutations, mapState } from 'vuex';
import BaseTable from '../../base-table';
import ItemTemplatesWorker from './item-templates-worker';
import ComponentAddTemplateWorker from './component_add_template_worker';

export default {
  name: 'TableTemplatesWorker',
  components: {
    ComponentAddTemplateWorker,
    ItemTemplatesWorker,
    BaseTable,
  },
  data() {
    return {
      snackbarDeleted: false,
      snackbarEdited: false,
      snackbarCreated: false,
    };
  },
  computed: {
    ...mapState('moduleTemplates', {
      paginationComputed: 'paginationWorker',
    }),
  },
  methods: {
    ...mapMutations('moduleTemplates', {
      functionSetPagination: 'setPaginationWorker',
    }),
  },
};
</script>

<style scoped>

</style>
