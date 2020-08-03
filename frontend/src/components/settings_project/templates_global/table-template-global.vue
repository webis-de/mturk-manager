<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div>
    <base-table
      title="Global templates"

      name-vuex-module="moduleTemplates"
      name-state-pagination="paginationGlobal"
      name-local-storage-pagination="pagination_templates_global"

      v-bind:function-load-page="loadPage"
      v-bind:array-items="arrayItems"

      name-state-columns="arrayColumns"
      name-state-columns-selected="objectColumnsSelectedInitial"

      v-bind:show-select="false"
    >
      <template
        v-slot:default="{ item, isCondensed }"
      >
        <item-templates-global
          v-bind:item="item"
          v-bind:is-condensed="isCondensed"

          v-on:edited="snackbarEdited = true"
          v-on:deleted="snackbarDeleted = true"
        />
      </template>

      <template v-slot:actions>
        <component-add-template-global
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
import { ServiceTemplates } from '../../../services/templates.service';
import BaseTable from '../../base-table';
import ItemTemplatesGlobal from './item-templates-global';
import ComponentAddTemplateGlobal from './component_add_template_global';

export default {
  name: 'TableTemplatesGlobal',
  components: {
    ComponentAddTemplateGlobal,
    ItemTemplatesGlobal,
    BaseTable,
  },
  data() {
    return {
      loadPage: ServiceTemplates.loadPageGlobal,

      snackbarDeleted: false,
      snackbarEdited: false,
      snackbarCreated: false,
    };
  },
  computed: {
    arrayItems() {
      const { arrayItemsGlobal } = this.$store.state.moduleTemplates;

      return arrayItemsGlobal === null ? [] : arrayItemsGlobal;
    },
    ...mapState('moduleTemplates', {
      arrayColumns: 'arrayColumns',
    }),
    ...mapState('moduleTemplates', {
      paginationComputed: 'paginationGlobal',
    }),
  },
  methods: {
    ...mapMutations('moduleTemplates', {
      functionSetPagination: 'setPaginationGlobal',
    }),
  },
};
</script>

<style scoped>

</style>
