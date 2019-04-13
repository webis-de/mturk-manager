<template>
  <div>
    <v-layout>
      <v-flex>
        <v-tabs
          v-model="indexTab"
        >
          <v-tab key="batch">
            Batches
          </v-tab>
          <v-tab key="hits">
            HITs
          </v-tab>
          <v-tab key="assignments">
            Assignments
          </v-tab>

          <v-tabs-items>
            <v-tab-item
              key="batches"
            >
              <v-card class="pa-1">
                <list-batches
                  name-state-pagination="paginationFinances"
                  name-local-storage-pagination="pagination_batches_finances"

                  name-local-storage-columns-selected="array_columns_batches_finances"
                  name-state-columns-selected="array_columns_selected_finances"
                  name-state-columns-selected-initial="array_columns_selected_initial_finances"

                  v-bind:filters="filtersBatches"
                  name-state-filters="objectFiltersFinances"
                  name-local-storage-filters="filtersBatchesFinances"
                ></list-batches>
              </v-card>
            </v-tab-item>

            <v-tab-item
              key="hits"
            >
              <v-card class="pa-1">
                <list-hits
                  name-state-pagination="paginationFinances"
                  name-local-storage-pagination="pagination_hits_finances"

                  name-local-storage-columns-selected="array_columns_hits_finances"
                  name-state-columns-selected="array_columns_selected_finances"
                  name-state-columns-selected-initial="array_columns_selected_initial_finances"

                  v-bind:filters="filtersHITs"
                  name-state-filters="objectFiltersFinances"
                  name-local-storage-filters="filtersHITsFinances"
                ></list-hits>
              </v-card>
            </v-tab-item>

            <v-tab-item
              key="assignment"
            >
              <v-card class="pa-1">
                <list-assignments
                  name-state-pagination="paginationFinances"
                  name-local-storage-pagination="pagination_assignments_finances"

                  name-local-storage-columns-selected="array_columns_assignments_finances"
                  name-state-columns-selected="array_columns_selected_finances"
                  name-state-columns-selected-initial="array_columns_selected_initial_finances"

                  v-bind:filters="filtersAssignments"
                  name-state-filters="objectFiltersFinances"
                  name-local-storage-filters="filtersAssignmentsFinances"
                ></list-assignments>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-tabs>
      </v-flex>
    </v-layout>

    <v-divider class="my-3"></v-divider>
    <v-container
      fluid
      class="pa-0 grid-list-lg"
    >
      <v-layout>
        <v-flex
          shrink
        >
          <display-expenses
            v-bind:expenses="expenses"
            v-bind:type-item="typeItem"
          ></display-expenses>
        </v-flex>

        <v-flex
          shrink
        >
          <v-card>
            <v-card-title>
              Current Balance
            </v-card-title>

            <v-card-text>
              <component-show-balance></component-show-balance>
            </v-card-text>
          </v-card>
        </v-flex>

      </v-layout>
    </v-container>
    <!--<v-divider class="my-3"></v-divider>-->
    <!--<div style="max-width: 100%">-->
    <!--<v-flex>-->
    <!--&lt;!&ndash;<component-show-batches></component-show-batches>&ndash;&gt;-->
    <!--</v-flex>-->
    <!--</div>-->
  </div>
</template>

<script>
import {
  mapState, mapGetters, mapMutations, mapActions,
} from 'vuex';

import ComponentShowBalance from '../../../components/finances/component-show-balance';
import DisplayExpenses from '../../../components/finances/display-expenses';
import ListBatches from '../../../components/batches/list/list-batches';
import { updateSandbox } from '../../../mixins/update-sandbox.mixin';
import ListHits from '../../../components/hits/list/list-hits';
import ListAssignments from '../../../components/assignments/list/list-assignments';
import { ServiceFinances } from '../../../services/finances.service';

export default {
  name: 'AppFinances',
  components: {
    ListAssignments,
    ListHits,
    ListBatches,
    ComponentShowBalance,
    // ComponentListBatches,
    DisplayExpenses,
  },
  mixins: [
    updateSandbox,
    // load_data,
  ],
  data() {
    return {
      indexTab: 0,
      expenses: {},
    };
  },
  computed: {
    activeFilters() {
      switch (this.typeItem) {
        case 'assignments':
          return this.filtersAssignments;
        case 'hits':
          return this.filtersHITs;
        case 'batches':
        default:
          return this.filtersBatches;
      }
    },
    typeItem() {
      switch (this.indexTab) {
        case 0:
          return 'batches';
        case 1:
          return 'hits';
        case 2:
        default:
          return 'assignments';
      }
    },
    ...mapState('moduleBatches', {
      filtersBatches: 'objectFiltersFinances',
    }),

    ...mapState('moduleHITs', {
      filtersHITs: 'objectFiltersFinances',
    }),

    ...mapState('moduleAssignments', {
      filtersAssignments: 'objectFiltersFinances',
    }),
  },
  watch: {
    activeFilters() {
      this.loadExpenses();
    },
  },
  created() {
    ServiceFinances.load_balance();
    this.loadExpenses();
  },
  methods: {
    loadExpenses() {
      this.expenses = {};
      ServiceFinances.load({
        filters: this.activeFilters,
        typeItem: this.typeItem,
      }).then((expenses) => {
        this.expenses = expenses;
      });
    },
    sandboxUpdated() {
      ServiceFinances.load_balance();
      this.loadExpenses();
    },
    ...mapActions('moduleBatches', {
      functionResetArrayColumnsBatches: 'reset_array_columns_finances',
    }),
    ...mapMutations('moduleBatches', {
      functionSetArrayColumnsBatches: 'set_array_columns_finances',
      functionSetPaginationBatches: 'setPaginationFinances',
    }),

    ...mapActions('moduleHITs', {
      functionResetArrayColumnsHITs: 'reset_array_columns_finances',
    }),
    ...mapMutations('moduleHITs', {
      functionSetArrayColumnsHITs: 'set_array_columns_finances',
      functionSetPaginationHITs: 'setPaginationFinances',
    }),

    ...mapActions('moduleAssignments', {
      functionResetArrayColumnsAssignments: 'reset_array_columns_finances',
    }),
    ...mapMutations('moduleAssignments', {
      functionSetArrayColumnsAssignments: 'set_array_columns_finances',
      functionSetPaginationAssignments: 'setPaginationFinances',
    }),
  },
};
</script>
