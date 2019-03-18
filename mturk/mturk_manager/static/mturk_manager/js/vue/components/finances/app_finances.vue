<template>
  <div>
    <!-- <v-layout wrap>
        <v-flex xs12 md6>
            <component-show-money-spent></component-show-money-spent>
        </v-flex>

        <v-flex xs12 md6 text-md-right>
        </v-flex>
    </v-layout> -->
    <v-layout>
      <v-flex>
        <h1 class="headline">Finances</h1>
      </v-flex>
      <v-flex
        class="text-xs-right"
      >
        <component-show-balance></component-show-balance>
      </v-flex>
    </v-layout>

    <v-layout>
      <v-flex>
        <v-tabs  >
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
                v-bind:function-reset-array-columns="functionResetArrayColumnsBatches"
                v-bind:function-set-array-columns="functionSetArrayColumnsBatches"
                v-bind:array-columns-selected="arrayColumnsSelectedBatches"

                v-bind:function-set-pagination="functionSetPaginationBatches"
                v-bind:pagination-computed="paginationComputedBatches"
              ></list-batches>
              </v-card>
          </v-tab-item>

          <v-tab-item
            key="hits"
          >
            <v-card class="pa-1">
              <list-hits
                v-bind:function-reset-array-columns="functionResetArrayColumnsHITs"
                v-bind:function-set-array-columns="functionSetArrayColumnsHITs"
                v-bind:array-columns-selected="arrayColumnsSelectedHITs"

                v-bind:function-set-pagination="functionSetPaginationHITs"
                v-bind:pagination-computed="paginationComputedHITs"
              ></list-hits>
            </v-card>
          </v-tab-item>

          <v-tab-item
            key="assignment"
          >
            <v-card class="pa-1">
              <list-assignments
                v-bind:function-reset-array-columns="functionResetArrayColumnsAssignments"
                v-bind:function-set-array-columns="functionSetArrayColumnsAssignments"
                v-bind:array-columns-selected="arrayColumnsSelectedAssignments"

                v-bind:function-set-pagination="functionSetPaginationAssignments"
                v-bind:pagination-computed="paginationComputedAssignments"
              ></list-assignments>
            </v-card>
          </v-tab-item>
            </v-tabs-items>
        </v-tabs>

      </v-flex>
    </v-layout>

    <v-divider class="my-3"></v-divider>
    <v-layout
      justify-end
    >
      <v-flex
        shrink
      >
        <display-expenses></display-expenses>
      </v-flex>
    </v-layout>
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

import ComponentShowBalance from './component-show-balance.vue';
import ComponentShowMoneySpent from './component-show-money-spent.vue';
import ComponentShowBatches from './component-show-batches.vue';
import DisplayExpenses from './display-expenses.vue';
import slug_project from '../../mixins/slug_project';
import ListBatches from '../batches/list/list-batches';
import { update_sandbox } from '../../mixins/update_sandbox';
import ListHits from '../hits/list/list-hits';
import ListAssignments from '../assignments/list/list-assignments';
import { ServiceFinances } from '../../services/finances.service';

export default {
  name: 'AppFinances',
  mixins: [
    slug_project,
    update_sandbox,
    // load_data,
  ],
  data() {
    return {
      // dialog: false,
      // drawer: false,
      // is_refreshing: true,
      // show_snackbar: false,
      // text_snackbar: 'Finished refreshing the data',
    };
  },
  methods: {
    sandbox_updated() {
      ServiceFinances.load_balance();
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
  computed: {
    ...mapGetters('moduleBatches', {
      arrayColumnsSelectedBatches: 'get_array_columns_selected_finances',
    }),
    ...mapState('moduleBatches', {
      paginationComputedBatches: 'paginationFinances',
    }),

    ...mapGetters('moduleHITs', {
      arrayColumnsSelectedHITs: 'get_array_columns_selected_general',
    }),
    ...mapState('moduleHITs', {
      paginationComputedHITs: 'paginationFinances',
    }),

    ...mapGetters('moduleAssignments', {
      arrayColumnsSelectedAssignments: 'get_array_columns_selected_general',
    }),
    ...mapState('moduleAssignments', {
      paginationComputedAssignments: 'paginationFinances',
    }),
  },
  created() {
    ServiceFinances.load_balance();
    ServiceFinances.load();
  },

  components: {
    ListAssignments,
    ListHits,
    ListBatches,
    ComponentShowBalance,
    ComponentShowMoneySpent,
    ComponentShowBatches,
    // ComponentListBatches,
    DisplayExpenses,
  },
};
</script>
