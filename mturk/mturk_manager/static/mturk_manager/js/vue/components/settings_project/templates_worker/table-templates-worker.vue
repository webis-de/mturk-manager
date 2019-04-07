<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div>
    <base-table
      v-bind:array-items="arrayItems"
      v-bind:array-columns="arrayColumns"
      v-bind:array-columns-selected="[
        'name',
        'height_frame',
        'count_parameters',
        'template_assignment',
        'template_hit',
        'template_global',
        'actions',
      ]"
      v-bind:function-load-page="function_load_page"
      v-bind:is-condensed="true"

      v-bind:pagination-computed="paginationComputed"
      v-bind:function-set-pagination="functionSetPagination"
    >
      <template
        v-slot:default="{ props, array_columns_selected, isCondensed }"
      >
        <item-templates-worker
          v-bind:props="props"
          v-bind:is-condensed="isCondensed"

          v-on:edited="snackbarEdited = true"
          v-on:deleted="snackbarDeleted = true"
        />
      </template>

      <template v-slot:actions>
        <component-add-template-worker
          v-on:created="snackbarCreated = true"
        ></component-add-template-worker>
      </template>
    </base-table>

    <v-snackbar
      v-model="snackbarDeleted"
      v-bind:timeout="1500"
      color="info"
      bottom
    >
      <v-spacer></v-spacer>
      Deleted!
      <v-spacer></v-spacer>
    </v-snackbar>

    <v-snackbar
      v-model="snackbarCreated"
      v-bind:timeout="1500"
      bottom
      color="info"
    >
      <v-spacer></v-spacer>
      Saved!
      <v-spacer></v-spacer>
    </v-snackbar>

    <v-snackbar
      v-model="snackbarEdited"
      v-bind:timeout="1500"
      bottom
      color="info"
    >
      <v-spacer></v-spacer>
      Updated!
      <v-spacer></v-spacer>
    </v-snackbar>
  </div>
</template>

<script>
import BaseTable from '../../base-table';
import {mapGetters, mapMutations, mapState} from 'vuex';
import { Service_Templates } from '../../../services/service_templates';
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
      function_load_page: Service_Templates.loadPageWorker,

      snackbarDeleted: false,
      snackbarEdited: false,
      snackbarCreated: false,
    };
  },
  computed: {
    ...mapState('moduleTemplates', {
      arrayItems: 'arrayItemsWorker',
      arrayColumns: 'arrayColumnsWorker',
    }),
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
