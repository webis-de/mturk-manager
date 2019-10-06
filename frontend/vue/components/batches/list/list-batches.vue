<template>
  <base-table
    name-vuex-module="moduleBatches"
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
  >
    <template v-slot:default="{ item, objectColumnsSelected, isCondensed }">
      <component-item-batch
        v-bind:item="item"
        v-bind:object-columns-selected="objectColumnsSelected"
        v-bind:show_links="showLinks"
        v-bind:is-condensed="isCondensed"
      />
    </template>

    <template v-slot:filters="{ filters, filtersActive }">
      <filters-table-batches
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
import {
  mapActions, mapGetters, mapMutations, mapState,
} from 'vuex';
import { Service_Batches as ServiceBatches } from '../../../services/service_batches';
import BaseTable from '../../base-table';
import ComponentItemBatch from './component_item_batch';
import FiltersTableBatches from './filters-table-batches';

export default {
  name: 'ListBatches',
  components: { FiltersTableBatches, ComponentItemBatch, BaseTable },
  props: {
    nameStatePagination: {
      required: false,
      type: String,
      default: 'paginationGeneral',
    },
    nameLocalStoragePagination: {
      required: false,
      type: String,
      default: 'pagination_batches_general',
    },

    nameStateColumns: {
      required: false,
      type: String,
      default: 'array_columns_general',
    },
    nameLocalStorageColumnsSelected: {
      required: false,
      type: String,
      default: 'array_columns_batches_general',
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
      default: 'object_batches_selected',
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
      default: 'filtersBatchesGeneral',
    },
  },
  data() {
    return {
      loadPage: ServiceBatches.load_page,
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
        arrayItems = this.$store.state.moduleBatches.arrayBatchesSandbox;
      } else {
        arrayItems = this.$store.state.moduleBatches.arrayBatches;
      }

      return arrayItems === null ? [] : arrayItems;
    },
    ...mapState('moduleBatches', {
      filtersGeneral: 'objectFiltersGeneral',
      filtersDefaultGeneral: 'objectFiltersDefaultGeneral',
    }),
  },
  methods: {
    ...mapActions('moduleBatches', {
      function_reset_array_columns_general: 'reset_array_columns_general',
      setState: 'setState',
    }),
    ...mapMutations('moduleBatches', {
      function_set_items_selected: 'set_batches_selected',
      function_clear_items_selected: 'clear_batches_selected',
      function_set_array_columns_general: 'set_array_columns_general',
    }),
  },
};
</script>

<style scoped></style>
