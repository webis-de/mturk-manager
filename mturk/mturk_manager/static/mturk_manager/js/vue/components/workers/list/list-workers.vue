<template>
  <base-table
    v-slot="{ props, array_columns_selected, isCondensed }"
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
  >
    <component-item-worker
      v-bind:props="props"
      v-bind:array_columns_selected="array_columns_selected"
      v-bind:show_links="showLinks"
      v-bind:is-condensed="isCondensed"
    />
  </base-table>

  <!--</v-layout>-->
  <!--&lt;!&ndash; select-all &ndash;&gt;-->
  <!--&lt;!&ndash; v-bind:rows-per-page-items="items_per_page" &ndash;&gt;-->
  <!--&lt;!&ndash;v-bind:search="search"&ndash;&gt;-->
  <!--&lt;!&ndash;<v-data-table&ndash;&gt;-->
  <!--&lt;!&ndash;select-all&ndash;&gt;-->
  <!--&lt;!&ndash;v-bind:headers="list_headers"&ndash;&gt;-->
  <!--&lt;!&ndash;v-bind:items="array_workers_prepared"&ndash;&gt;-->
  <!--&lt;!&ndash;v-bind:pagination.sync="pagination"&ndash;&gt;-->
  <!--&lt;!&ndash;v-bind:total-items="items_total"&ndash;&gt;-->
  <!--&lt;!&ndash;v-model="workers_selected"&ndash;&gt;-->
  <!--&lt;!&ndash;&gt;&ndash;&gt;-->
  <!--&lt;!&ndash;<template slot="headers" slot-scope="props">&ndash;&gt;-->
  <!--&lt;!&ndash;<tr class="row_header">&ndash;&gt;-->
  <!--&lt;!&ndash;<th>&ndash;&gt;-->
  <!--&lt;!&ndash;<v-checkbox&ndash;&gt;-->
  <!--&lt;!&ndash;v-bind::input-value="props.all"&ndash;&gt;-->
  <!--&lt;!&ndash;v-bind::indeterminate="props.indeterminate"&ndash;&gt;-->
  <!--&lt;!&ndash;primary&ndash;&gt;-->
  <!--&lt;!&ndash;hide-details&ndash;&gt;-->
  <!--&lt;!&ndash;v-on:click.native="toggleAll"&ndash;&gt;-->
  <!--&lt;!&ndash;&gt;</v-checkbox>&ndash;&gt;-->
  <!--&lt;!&ndash;</th>&ndash;&gt;-->
  <!--&lt;!&ndash;<th&ndash;&gt;-->
  <!--&lt;!&ndash;v-for="header in props.headers"&ndash;&gt;-->
  <!--&lt;!&ndash;v-bind:key="header.value"&ndash;&gt;-->
  <!--&lt;!&ndash;v-bind:width="header.width"&ndash;&gt;-->
  <!--&lt;!&ndash;v-bind:class="[&ndash;&gt;-->
  <!--&lt;!&ndash;'column sortable', &ndash;&gt;-->
  <!--&lt;!&ndash;pagination.descending ? 'desc' : 'asc', &ndash;&gt;-->
  <!--&lt;!&ndash;header.value === pagination.sortBy ? 'active' : ''&ndash;&gt;-->
  <!--&lt;!&ndash;]"&ndash;&gt;-->
  <!--&lt;!&ndash;v-on:click="changeSort(header.value)"&ndash;&gt;-->
  <!--&lt;!&ndash;&gt;&ndash;&gt;-->
  <!--&lt;!&ndash;<v-icon small>arrow_upward</v-icon>&ndash;&gt;-->
  <!--&lt;!&ndash;{{ header.text }}&ndash;&gt;-->
  <!--&lt;!&ndash;</th>&ndash;&gt;-->
  <!--&lt;!&ndash;</tr>&ndash;&gt;-->
  <!--&lt;!&ndash;</template>&ndash;&gt;-->

  <!--&lt;!&ndash;<template&ndash;&gt;-->
  <!--&lt;!&ndash;slot="items"&ndash;&gt;-->
  <!--&lt;!&ndash;slot-scope="props"&ndash;&gt;-->
  <!--&lt;!&ndash;&gt;&ndash;&gt;-->
  <!--&lt;!&ndash;<component-item-worker&ndash;&gt;-->
  <!--&lt;!&ndash;v-bind:props="props"&ndash;&gt;-->
  <!--&lt;!&ndash;&gt;&ndash;&gt;-->
  <!--&lt;!&ndash;</component-item-worker>&ndash;&gt;-->
  <!--&lt;!&ndash;</template>&ndash;&gt;-->
  <!--&lt;!&ndash;</v-data-table>&ndash;&gt;-->
  <!--&lt;!&ndash; {{list_workers}} &ndash;&gt;-->
  <!--</span>-->
  <!-- </v-layout> -->

  <!-- <v-data-table
        v-bind:items="list_workers"
        v-bind:headers="list_headers"
        disable-initial-sort
        v-bind:pagination.sync="pagination"
        v-model="workers_selected"
        select-all
        item-key="name"
        class="elevation-1"
    >
         <template slot="items" slot-scope="props">
            <td>
                <v-checkbox
                    v-model="props.selected"
                    primary
                    hide-details
                ></v-checkbox>
            </td>
            <td>{{ props.item.name }}</td>
            <td class="justify-end layout">
                <v-btn icon class="mx-0" v-on:click="init_edit_policy(props.item)">
                    <v-icon color="teal">edit</v-icon>
                </v-btn>
                <v-btn icon class="mx-0" v-on:click="delete_policy(props.item)">
                    <v-icon color="pink">delete</v-icon>
                </v-btn>
            </td>
        </template>
    </v-data-table> -->
</template>
<script>
  import {
    mapActions, mapGetters, mapMutations, mapState,
  } from 'vuex';
// import { Policy } from '../../store/modules/policies.js';
import ComponentItemWorker from './component_item_worker';
import { Service_Workers as ServiceWorkers } from '../../../services/service_worker';
import { update_sandbox as updateSandbox } from '../../../mixins/update_sandbox';
import externalPagination from '../../../mixins/external_pagination';
import { table } from '../../../mixins/table';
import BaseTable from '../../base-table';
// import ComponentShowMoneySpent from './component-show-money-spent.vue';
// import ComponentShowBatches from './component-show-batches.vue';
export default {
  name: 'ComponentListWorkers',
  components: {
    BaseTable,
    ComponentItemWorker,
  },
  mixins: [updateSandbox, externalPagination, table],
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

      filters: {
        id_worker: '',
        show_workers_blocked_none: true,
        show_workers_blocked_limit: true,
        show_workers_blocked_soft: true,
        show_workers_blocked_hard: true,
      },

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
