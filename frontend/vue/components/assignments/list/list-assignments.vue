<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <base-table
    title="Assignments"

    name-vuex-module="moduleAssignments"
    v-bind:name-state-pagination="nameStatePagination"
    v-bind:name-local-storage-pagination="nameLocalStoragePagination"

    v-bind:function-load-page="loadPage"
    v-bind:array-items="arrayItems"

    v-bind:name-local-storage-columns-selected="nameLocalStorageColumnsSelected"
    v-bind:name-state-columns="nameStateColumns"
    v-bind:name-state-columns-selected="nameStateColumnsSelected"
    v-bind:name-state-columns-selected-initial="nameStateColumnsSelectedInitial"

    v-bind:name-state-items-selected="nameStateItemsSelected"


    v-bind:function-set-items-selected="function_set_items_selected"
    v-bind:function-clear-items-selected="function_clear_items_selected"

    v-bind:filters="filtersComputed"
    v-bind:filters-default="filtersDefaultComputed"
    v-bind:set-state="setState"
    v-bind:name-state-filters="nameStateFilters"
    v-bind:name-local-storage-filters="nameLocalStorageFilters"

    v-on:changed-selection="changedSelection"
  >
    <template v-slot:default="{ item, objectColumnsSelected, isCondensed, changedSelection, itemsSelected }">
      <component-item-assignment
        v-bind:item="item"
        v-bind:object-columns-selected="objectColumnsSelected"
        v-bind:show_links="showLinks"
        v-bind:is-condensed="isCondensed"
        v-bind:items-selected="itemsSelected"
        v-on:changed-selection="changedSelection"
      />
    </template>

    <template v-slot:filters="{ filters, filtersActive }">
      <filters-table-assignments
        v-bind:filters="filters"
        v-bind:filters-active="filtersActive"
      ></filters-table-assignments>
    </template>

    <template v-slot:actions>
      <slot name="actions"/>
    </template>
  </base-table>
</template>
<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex';
import { Service_Assignments as ServiceAssignments } from '../../../services/service_assignments';
import BaseTable from '../../base-table';
import ComponentItemAssignment from './component_item_assignment';
import FiltersTableAssignments from './filters-table-assignments';

export default {
  name: 'ListAssignments',
  components: {FiltersTableAssignments, ComponentItemAssignment, BaseTable },
  props: {
    nameStatePagination: {
      required: false,
      type: String,
      default: 'paginationGeneral',
    },
    nameLocalStoragePagination: {
      required: false,
      type: String,
      default: 'pagination_assignments_general',
    },

    nameStateColumns: {
      required: false,
      type: String,
      default: 'array_columns_general',
    },
    nameLocalStorageColumnsSelected: {
      required: false,
      type: String,
      default: 'array_columns_assignments_general',
    },
    nameStateColumnsSelected: {
      required: false,
      type: String,
      default: 'objectColumnsSelectedGeneral',
    },
    nameStateColumnsSelectedInitial: {
      required: false,
      type: String,
      default: 'objectColumnsSelectedInitialGeneral',
    },

    nameStateItemsSelected: {
      required: false,
      type: String,
      default: 'object_assignments_selected',
    },


    showLinks: {
      required: false,
      type: Boolean,
      default: true,
    },

    filters: {
      required: false,
      type: Object,
      default: undefined,
    },
    filtersDefault: {
      required: false,
      type: Object,
      default: undefined,
    },
    nameStateFilters: {
      required: false,
      type: String,
      default: 'objectFiltersGeneral',
    },
    nameLocalStorageFilters: {
      required: false,
      type: String,
      default: 'filtersAssignmentsGeneral',
    },
  },
  data() {
    return {
      loadPage: ServiceAssignments.load_page,
    };
  },
  computed: {
    filtersComputed() {
      return this.filters !== undefined ? this.filters : this.filtersGeneral;
    },
    filtersDefaultComputed() {
      return this.filtersDefault !== undefined ? this.filtersDefault : this.filtersDefaultGeneral;
    },
    arrayItems() {
      let arrayItems = [];

      if (this.$store.state.module_app.use_sandbox === true) {
        arrayItems = this.$store.state.moduleAssignments.arrayAssignmentsSandbox;
      } else {
        arrayItems = this.$store.state.moduleAssignments.arrayAssignments;
      }

      return arrayItems === null ? [] : arrayItems;
    },
    ...mapState('moduleAssignments', {
      filtersGeneral: 'objectFiltersGeneral',
      filtersDefaultGeneral: 'objectFiltersDefaultGeneral',
    }),
  },
  methods: {
    changedSelection(itemsSelected) {
      // this.$store.dispatch('moduleBatches/setItemsSelected', {
      //   items: itemsSelected,
      // });
    },
    ...mapActions('moduleAssignments', {
      function_reset_array_columns: 'reset_array_columns_general',
      setState: 'setState',
    }),
    ...mapMutations('moduleAssignments', {
      function_set_items_selected: 'set_assignments_selected',
      function_clear_items_selected: 'clear_assignments_selected',
      function_set_array_columns: 'set_array_columns_general',
    }),
  },
};
</script>

<style scoped></style>
