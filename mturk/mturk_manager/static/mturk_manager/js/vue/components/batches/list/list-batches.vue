<template>
  <base-table
    v-bind:array-items="array_items"
    v-bind:array-columns="array_columns"
    v-bind:array-columns-selected="array_columns_selected_computed"
    v-bind:function-reset-array-columns="function_reset_array_columns_computed"
    v-bind:function-set-array-columns="function_set_array_columns_computed"
    v-bind:function-load-page="function_load_page"
    v-bind:object-items-selected="object_items_selected"
    v-bind:function-set-items-selected="function_set_items_selected"
    v-bind:function-clear-items-selected="function_clear_items_selected"

    v-bind:pagination-computed="paginationComputed"
    v-bind:function-set-pagination="functionSetPagination"

    v-bind:filters="filters"
    v-bind:filters-default="filtersDefault"
    name-state-filters="objectFiltersGeneral"
    name-local-storage-filters="filtersBatchesGeneral"
  >
    <template v-slot:default="{ props, array_columns_selected, isCondensed }">
      <component-item-batch
        v-bind:props="props"
        v-bind:array_columns_selected="array_columns_selected"
        v-bind:show_links="showLinks"
        v-bind:is-condensed="isCondensed"
      />
    </template>

    <template v-slot:filters="{ filters, filtersActive }">
      <filters-table-batches
        v-bind:filters="filters"
        v-bind:filters-active="filtersActive"
      ></filters-table-batches>
    </template>

    <template v-slot:actions>
      <slot name="actions"></slot>
    </template>
  </base-table>
</template>

<script>
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex';
import { Service_Batches as ServiceBatches } from '../../../services/service_batches';
import BaseTable from '../../base-table';
import ComponentItemBatch from './component_item_batch';
import FiltersTableBatches from './filters-table-batches';

export default {
  name: 'ListBatches',
  components: {FiltersTableBatches, ComponentItemBatch, BaseTable },
  props: {
    showLinks: {
      required: false,
      type: Boolean,
      default: true,
    },
    functionResetArrayColumns: {
      required: false,
      type: Function,
      default: undefined,
    },
    functionSetArrayColumns: {
      required: false,
      type: Function,
      default: undefined,
    },
    arrayColumnsSelected: {
      required: false,
      type: Array,
      default: undefined,
    },

    paginationComputed: {
      type: Object,
      required: true,
    },
    functionSetPagination: {
      type: Function,
      required: true,
    },
  },
  data() {
    return {
      function_load_page: ServiceBatches.load_page,
    };
  },
  computed: {
    function_reset_array_columns_computed() {
      return this.functionResetArrayColumns !== undefined
        ? this.functionResetArrayColumns
        : this.function_reset_array_columns_general;
    },
    function_set_array_columns_computed() {
      return this.functionSetArrayColumns !== undefined
        ? this.functionSetArrayColumns
        : this.function_set_array_columns_general;
    },
    array_columns_selected_computed() {
      return this.arrayColumnsSelected !== undefined
        ? this.arrayColumnsSelected
        : this.array_columns_selected_general;
    },
    ...mapGetters('moduleBatches', {
      array_items: 'get_array_batches',
      object_items_selected: 'get_object_batches_selected',
      array_columns: 'get_array_columns_general',
      array_columns_selected_general: 'get_array_columns_selected_general',
    }),
    ...mapState('moduleBatches', {
      filters: 'objectFiltersGeneral',
      filtersDefault: 'objectFiltersDefaultGeneral',
    }),
  },
  methods: {
    ...mapActions('moduleBatches', {
      function_reset_array_columns_general: 'reset_array_columns_general',
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
