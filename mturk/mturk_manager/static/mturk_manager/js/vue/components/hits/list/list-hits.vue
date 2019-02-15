<template>
  <base-table
    v-bind:array_items="array_items"
    v-bind:array_columns="array_columns"
    v-bind:array_columns_selected="array_columns_selected"
    v-bind:function_reset_array_columns="function_reset_array_columns"
    v-bind:function_set_array_columns="function_set_array_columns"
    v-bind:function_load_page="function_load_page"
    v-bind:object_items_selected="object_items_selected"
    v-bind:function_set_items_selected="function_set_items_selected"
    v-bind:function_clear_items_selected="function_clear_items_selected"
    v-bind:filters="{
      id_batch
    }"
    v-slot="{ props, array_columns_selected, isCondensed }"
  >
    <component-item-hit
      v-bind:props="props"
      v-bind:array_columns_selected="array_columns_selected"
      v-bind:show_links="show_links"
      v-bind:is-condensed="isCondensed"
    ></component-item-hit>
  </base-table>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { Service_HITs } from '../../../services/service_hits';
import BaseTable from '../../base-table';
import ComponentItemHit from './component_item_hit';

export default {
  name: 'list-hits',
  components: { ComponentItemHit, BaseTable },
  props: {
    id_batch: {
      required: false,
      type: Number,
    },
    show_links: {
      required: false,
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      function_load_page: Service_HITs.load_page,
    };
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
  computed: {
    ...mapGetters('moduleHITs', {
      array_items: 'get_array_hits',
      object_items_selected: 'get_object_hits_selected',
      array_columns: 'get_array_columns_general',
      array_columns_selected: 'get_array_columns_selected_general',
    }),
  },
};
</script>

<style scoped></style>
