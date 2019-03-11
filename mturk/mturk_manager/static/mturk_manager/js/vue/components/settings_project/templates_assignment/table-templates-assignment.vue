<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div>
    <base-table
      v-bind:array-items="arrayItems"
      v-bind:array-columns="arrayColumns"
      v-bind:array-columns-selected="[
        'name',
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
        <item-templates-assignment
          v-bind:props="props"
          v-bind:is-condensed="isCondensed"

          v-on:edited="snackbarEdited = true"
          v-on:deleted="snackbarDeleted = true"
        />
      </template>

      <template v-slot:actions>
        <component-add-template-assignment
          v-on:created="snackbarCreated = true"
        ></component-add-template-assignment>
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
import {table} from '../../../mixins/table';
import {Service_Templates} from '../../../services/service_templates';
import {mapMutations, mapState} from 'vuex';
import ItemTemplatesAssignment from './item-templates-assignment';
import ComponentAddTemplateAssignment from './component_add_template_assignment';
import BaseTable from '../../base-table';

export default {
  name: 'TableTemplatesAssignment',
  components: {BaseTable, ComponentAddTemplateAssignment, ItemTemplatesAssignment},
  data() {
    return {
      function_load_page: Service_Templates.loadPageAssignment,

      snackbarDeleted: false,
      snackbarEdited: false,
      snackbarCreated: false,
    };
  },
  computed: {
    ...mapState('moduleTemplates', {
      arrayItems: 'arrayItemsAssignment',
      arrayColumns: 'arrayColumns',
    }),
    ...mapState('moduleTemplates', {
      paginationComputed: 'paginationAssignment',
    }),
  },
  methods: {
    ...mapMutations('moduleTemplates', {
      functionSetPagination: 'setPaginationAssignment',
    }),
  },
};
</script>

<style scoped>

</style>