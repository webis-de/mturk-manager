<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div>
    <base-table
      title="Requester templates"

      name-vuex-module="moduleTemplates"
      name-state-pagination="paginationAssignment"
      name-local-storage-pagination="pagination_templates_assignment"

      v-bind:function-load-page="loadPage"
      v-bind:array-items="arrayItems"

      name-state-columns="arrayColumns"
      name-state-columns-selected="objectColumnsSelectedInitial"

      v-bind:show-select="false"
    >
      <template
        v-slot:default="{ item, isCondensed }"
      >
        <item-templates-assignment
          v-bind:item="item"
          v-bind:is-condensed="isCondensed"

          v-on:edited="snackbarEdited = true"
          v-on:deleted="snackbarDeleted = true"
        />
      </template>

      <template v-slot:actions>
        <component-add-template-assignment
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
import { ServiceTemplates } from '../../../services/service_templates';
import ItemTemplatesAssignment from './item-templates-assignment';
import ComponentAddTemplateAssignment from './component_add_template_assignment';
import BaseTable from '../../base-table';

export default {
  name: 'TableTemplatesAssignment',
  components: { BaseTable, ComponentAddTemplateAssignment, ItemTemplatesAssignment },
  data() {
    return {
      loadPage: ServiceTemplates.loadPageAssignment,

      snackbarDeleted: false,
      snackbarEdited: false,
      snackbarCreated: false,
    };
  },
  created() {
    ServiceTemplates.loadPageHIT({
      page: 1,
      sortBy: ['name'],
      sortDesc: [false],
    });
    ServiceTemplates.loadPageGlobal({
      page: 1,
      sortBy: ['name'],
      sortDesc: [false],
    });
  },
  computed: {
    arrayItems() {
      const { arrayItemsAssignment, arrayItemsHIT, arrayItemsGlobal } = this.$store.state.moduleTemplates;

      if (arrayItemsAssignment === null || arrayItemsHIT === null || arrayItemsGlobal === null) {
        return [];
      }

      return arrayItemsAssignment.concat(arrayItemsHIT).concat(arrayItemsGlobal);
    },
    ...mapState('moduleTemplates', {
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
