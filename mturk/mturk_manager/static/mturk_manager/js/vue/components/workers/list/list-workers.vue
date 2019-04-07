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

    v-bind:function-set-pagination="functionSetPagination"
    v-bind:pagination-computed="paginationComputed"

    v-bind:filters="filters"
    v-bind:filters-default="filtersDefault"
    v-bind:set-state="setState"
    name-state-filters="objectFiltersGeneral"
    name-local-storage-filters="filtersWorkersGeneral"
  >
    <template v-slot:default="{ props, array_columns_selected, isCondensed }">
      <component-item-worker
        v-bind:props="props"
        v-bind:array_columns_selected="array_columns_selected"
        v-bind:show_links="showLinks"
        v-bind:is-condensed="isCondensed"
      />
    </template>

    <template v-slot:filters="{ filters, filtersActive }">
      <filters-table-workers
        v-bind:filters="filters"
        v-bind:filters-active="filtersActive"
      ></filters-table-workers>
    </template>
  </base-table>
</template>
<script>
  import {
    mapActions, mapGetters, mapMutations, mapState,
  } from 'vuex';
// import { Policy } from '../../store/modules/policies.js';
import ComponentItemWorker from './component_item_worker';
import { Service_Workers as ServiceWorkers } from '../../../services/service_worker';
import BaseTable from '../../base-table';
  import FiltersTableWorkers from './filters-table-workers';
// import ComponentShowMoneySpent from './component-show-money-spent.vue';
// import ComponentShowBatches from './component-show-batches.vue';
export default {
  name: 'ComponentListWorkers',
  components: {
    FiltersTableWorkers,
    BaseTable,
    ComponentItemWorker,
  },
  props: {
    showLinks: {
      required: false,
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      function_load_page: ServiceWorkers.load_page,
      workers_selected: [],
      pagination: { rowsPerPage: 5 },
      // pagination: { rowsPerPage: 5, totalItems: 30 },
      show_dialog_policy: false,
      policy_to_be_edited: null,

      items_total: undefined,
      // items_per_page: [12, 24],

      // filters: {
      //   id_worker: '',
      //   show_workers_blocked_none: true,
      //   show_workers_blocked_limit: true,
      //   show_workers_blocked_soft: true,
      //   show_workers_blocked_hard: true,
      // },

      // search: 'A10BOAO1EONNS7',
      // policy_new: new Policy({
      //     QualificationTypeStatus: 'Active',
      // }),

      list_headers: [
        {
          text: 'Name',
          value: 'name',
        },

        // {
        //     text: 'Approved (%)',
        //     value: 'percentage_approved_assignments',
        //     align: 'center',
        //     width: '1px'
        // },
        // {
        //     text: 'Rejected (%)',
        //     value: 'percentage_rejected_assignments',
        //     align: 'center',
        //     width: '1px'
        // },

        {
          text: 'Assignment Limit',
          value: 'counter_assignments',
          align: 'center',
          width: '1px',
        },
        {
          text: 'Project Block',
          value: 'block_soft',
          width: '1px',
        },
        {
          text: 'Soft MTurk Block',
          value: 'block_soft_hard',
          width: '1px',
        },
        {
          text: 'Hard MTurk Block',
          value: 'block_hard',
          width: '1px',
        },
      ],
    };
  },
  computed: {
    ...mapGetters('moduleWorkers', {
      array_items: 'get_array_workers',
      object_items_selected: 'get_object_workers_selected',
      array_columns: 'get_array_columns_general',
      array_columns_selected: 'get_array_columns_selected_general',
    }),
    list_workers() {
      return this.list_workers_processed.slice(0, 5);
    },
    // policy_dialog: function() {
    //     return this.policy_to_be_edited == null ? this.policy_new : this.policy_to_be_edited;
    // },
    // title_dialog_policy: function() {
    //     return this.policy_to_be_edited == null ? 'New Policy' : 'Edit Policy';
    // },
    ...mapGetters('moduleWorkers', {
      list_workers_processed: 'list_workers',
    }),
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
    ...mapState('moduleWorkers', {
      paginationComputed: 'paginationGeneral',
      filters: 'objectFiltersGeneral',
      filtersDefault: 'objectFiltersDefaultGeneral',
    }),
  },
  methods: {
    load_page() {
      this.loading = true;
      ServiceWorkers.load_page(this.pagination, {
        ...this.filters,
      }).then((itemsTotal) => {
        this.items_total = itemsTotal;
        this.loading = false;
      });
    },
    ...mapMutations('moduleWorkers', {
      function_set_items_selected: 'set_workers_selected',
      function_clear_items_selected: 'clear_workers_selected',
      function_set_array_columns: 'set_array_columns_general',
      functionSetPagination: 'setPaginationGeneral',
    }),
    ...mapActions('moduleWorkers', {
      update_status_block: 'update_status_block',
      function_reset_array_columns: 'reset_array_columns_general',
      setState: 'setState',
    }),
  },

};
</script>

<style lang="scss" scoped>
.row_header {
  height: 48px;
  // height: unset !important;
}
</style>
