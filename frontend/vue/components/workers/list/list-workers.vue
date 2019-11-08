<template>
  <base-table
    title="Workers"

    name-vuex-module="moduleWorkers"
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
    name-state-filters="objectFiltersGeneral"
    name-local-storage-filters="filtersWorkersGeneral"
  >
    <template v-slot:default="{ item, objectColumnsSelected, isCondensed }">
      <component-item-worker
        v-bind:item="item"
        v-bind:object-columns-selected="objectColumnsSelected"
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

    <template v-slot:actions>
      <slot name="actions"></slot>
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
  name: 'TableWorkers',
  components: {
    FiltersTableWorkers,
    BaseTable,
    ComponentItemWorker,
  },
  props: {
    nameStatePagination: {
      required: false,
      type: String,
      default: 'paginationGeneral',
    },
    nameLocalStoragePagination: {
      required: false,
      type: String,
      default: 'pagination_workers_general',
    },

    nameStateColumns: {
      required: false,
      type: String,
      default: 'array_columns_general',
    },
    nameLocalStorageColumnsSelected: {
      required: false,
      type: String,
      default: 'array_columns_workers_general',
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
      default: 'object_workers_selected',
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
      default: 'filtersWorkersGeneral',
    },


    showLinks: {
      required: false,
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      loadPage: ServiceWorkers.loadPage,
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
    filtersComputed() {
      return this.filters !== undefined ? this.filters : this.filtersGeneral;
    },
    filtersDefaultComputed() {
      return this.filtersDefault !== undefined ? this.filtersDefault : this.filtersDefaultGeneral;
    },
    arrayItems() {
      let arrayItems = [];

      if (this.$store.state.module_app.use_sandbox === true) {
        arrayItems = this.$store.state.moduleWorkers.arrayWorkersSandbox;
      } else {
        arrayItems = this.$store.state.moduleWorkers.arrayWorkers;
      }

      return arrayItems === null ? [] : arrayItems;
    },
    ...mapGetters('moduleWorkers', {
      object_items_selected: 'get_object_workers_selected',
      array_columns: 'get_array_columns_general',
      array_columns_selected: 'get_array_columns_selected_general',
    }),
    // policy_dialog: function() {
    //     return this.policy_to_be_edited == null ? this.policy_new : this.policy_to_be_edited;
    // },
    // title_dialog_policy: function() {
    //     return this.policy_to_be_edited == null ? 'New Policy' : 'Edit Policy';
    // },
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
    ...mapState('moduleWorkers', {
      paginationComputed: 'paginationGeneral',
      filtersGeneral: 'objectFiltersGeneral',
      filtersDefaultGeneral: 'objectFiltersDefaultGeneral',
    }),
  },
  methods: {
    load_page() {
      this.loading = true;
      ServiceWorkers.loadPage(this.pagination, {
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
