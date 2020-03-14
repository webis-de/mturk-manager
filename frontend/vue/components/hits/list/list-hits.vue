<template>
  <base-table
    title="HITs"

    name-vuex-module="moduleHITs"
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
      <component-item-hit
        v-bind:item="item"
        v-bind:object-columns-selected="objectColumnsSelected"
        v-bind:show_links="showLinks"
        v-bind:is-condensed="isCondensed"
        v-bind:items-selected="itemsSelected"
        v-on:changed-selection="changedSelection"
      />
    </template>

    <template v-slot:filters="{ filters, filtersActive }">
      <filters-table-hits
        v-bind:filters="filters"
        v-bind:filters-active="filtersActive"
      />
    </template>

    <template v-slot:actions>
      <slot name="actions"></slot>
    </template>
  </base-table>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from 'vuex';
import { Service_HITs as ServiceHits } from '../../../services/service_hits';
import BaseTable from '../../base-table';
import ComponentItemHit from './component_item_hit';
import FiltersTableHits from './filters-table-hits';

export default {
  name: 'ListHits',
  components: {FiltersTableHits, ComponentItemHit, BaseTable },
  props: {
    nameStatePagination: {
      required: false,
      type: String,
      default: 'paginationGeneral',
    },
    nameLocalStoragePagination: {
      required: false,
      type: String,
      default: 'pagination_hits_general',
    },

    nameStateColumns: {
      required: false,
      type: String,
      default: 'array_columns_general',
    },
    nameLocalStorageColumnsSelected: {
      required: false,
      type: String,
      default: 'array_columns_hits_general',
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
      default: 'object_hits_selected',
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
      default: 'filtersHITsGeneral',
    },
  },
  data() {
    return {
      loadPage: ServiceHits.load_page,
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
        arrayItems = this.$store.state.moduleHITs.arrayHITsSandbox;
      } else {
        arrayItems = this.$store.state.moduleHITs.arrayHITs;
      }

      return arrayItems === null ? [] : arrayItems;
    },
    ...mapState('moduleHITs', {
      filtersGeneral: 'objectFiltersGeneral',
      filtersDefaultGeneral: 'objectFiltersDefaultGeneral',
    }),
  },
  methods: {
    changedSelection(itemsSelected) {
      this.$store.dispatch('moduleHITs/setItemsSelected', {
        items: itemsSelected,
      });
    },
    ...mapActions('moduleHITs', {
      function_reset_array_columns: 'reset_array_columns_general',
      setState: 'setState',
    }),
    ...mapMutations('moduleHITs', {
      function_set_items_selected: 'set_hits_selected',
      function_clear_items_selected: 'clear_hits_selected',
      function_set_array_columns: 'set_array_columns_general',
    }),
  },
};
</script>

<style scoped></style>
