<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div>
    <base-table
      title="Worker templates"

      name-vuex-module="moduleTemplates"
      name-state-pagination="paginationWorker"
      name-local-storage-pagination="pagination_templates_worker"

      v-bind:function-load-page="loadPage"
      v-bind:array-items="arrayItems"

      name-state-columns="arrayColumnsWorker"
      name-state-columns-selected="objectColumnsSelectedInitialGeneral"

      v-bind:show-select="false"
    >
      <template
        v-slot:default="{ item, isCondensed }"
      >
        <item-templates-worker
          v-bind:item="item"
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
      loadPage: Service_Templates.loadPageWorker,

      snackbarDeleted: false,
      snackbarEdited: false,
      snackbarCreated: false,
    };
  },
  computed: {
    arrayItems() {
      const { arrayItemsWorker } = this.$store.state.moduleTemplates;

      return arrayItemsWorker === null ? [] : arrayItemsWorker;
    },
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
