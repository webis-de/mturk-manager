<template>
  <base-table
    v-bind:array-items="array_items"
    v-bind:array-columns="array_columns"
    v-bind:array-columns-selected="array_columns_selected"
    v-bind:function-reset-array-columns="function_reset_array_columns"
    v-bind:function-set-array-columns="function_set_array_columns"
    v-bind:function-load-page="function_load_page"
    v-bind:object-items-selected="object_items_selected"
    v-bind:function-set-items-selected="function_set_items_selected"
    v-bind:function-clear-items-selected="function_clear_items_selected"

    v-bind:pagination-computed="paginationComputed"
    v-bind:function-set-pagination="functionSetPagination"
  >
    <template v-slot="{ props, array_columns_selected, isCondensed }">
      <component-item-hit
        v-bind:props="props"
        v-bind:array_columns_selected="array_columns_selected"
        v-bind:show_links="showLinks"
        v-bind:is-condensed="isCondensed"
      />
    </template>

    <template v-slot:actions>
      <slot name="actions"></slot>
    </template>
  </base-table>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { Service_HITs as ServiceHits } from '../../../services/service_hits';
import BaseTable from '../../base-table';
import ComponentItemHit from './component_item_hit';

export default {
  name: 'ListHits',
  components: { ComponentItemHit, BaseTable },
  props: {
    showLinks: {
      required: false,
      type: Boolean,
      default: true,
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
      function_load_page: ServiceHits.load_page,
    };
  },
  computed: {
    ...mapGetters('moduleHITs', {
      array_items: 'get_array_hits',
      object_items_selected: 'get_object_hits_selected',
      array_columns: 'get_array_columns_general',
      array_columns_selected: 'get_array_columns_selected_general',
    }),
  },
  methods: {
    ...mapActions('moduleHITs', {
      function_reset_array_columns: 'reset_array_columns_general',
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
