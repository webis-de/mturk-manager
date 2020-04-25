<template>
  <div>
    <base-page>
      <!--      <base-page-section-->
      <!--        identifier="finances"-->
      <!--      >-->
      <!--        <v-row dense>-->
      <!--          <v-col>-->
      <!--            <h2 class="headline">-->
      <!--              Budget ($)-->
      <!--            </h2>-->
      <!--          </v-col>-->
      <!--        </v-row>-->
      <!--        <v-row-->
      <!--          dense-->
      <!--        >-->
      <!--          <v-col>-->
      <!--            <component-show-balance-->
      <!--              v-bind:expenses="expenses"-->
      <!--            />-->
      <!--          </v-col>-->
      <!--        </v-row>-->
      <!--      </base-page-section>-->

      <base-page-group
        v-bind:identifier="{
          identifier: 'finances',
          label: 'Finances'
        }"
      >
        <base-page-section
          shrink
          title="Batch costs"
        >
          <v-row dense>
            <v-col class="shrink">
              <display-expenses
                v-bind:expenses="expenses"
                type-item="batches"
              />
            </v-col>
          </v-row>
        </base-page-section>
        <base-page-section
          shrink
          title="HIT costs"
        >
          <v-row dense>
            <v-col class="shrink">
              <display-expenses
                v-bind:expenses="expenses"
                type-item="hits"
              />
            </v-col>
          </v-row>
        </base-page-section>
        <base-page-section
          shrink
          title="Assignment costs"
        >
          <v-row dense>
            <v-col>
              <display-expenses
                v-bind:expenses="expenses"
                type-item="assignments"
              />
            </v-col>
          </v-row>
        </base-page-section>
      </base-page-group>

      <base-page-section
        type="table"
        v-bind:identifier="{
          identifier: 'batches',
          label: 'Batches'
        }"
      >
        <list-batches
          name-state-pagination="paginationFinances"
          name-local-storage-pagination="pagination_batches_finances"

          name-local-storage-columns-selected="array_columns_batches_finances"
          name-state-columns-selected="objectColumnsSelectedFinances"
          name-state-columns-selected-initial="objectColumnsSelectedInitialFinances"

          v-bind:filters="filtersBatches"
          name-state-filters="objectFiltersFinances"
          name-local-storage-filters="filtersBatchesFinances"
        />
      </base-page-section>

      <base-page-section
        type="table"
        v-bind:identifier="{
          identifier: 'hits',
          label: 'HITs'
        }"
      >
        <list-hits
          name-state-pagination="paginationFinances"
          name-local-storage-pagination="pagination_hits_finances"

          name-local-storage-columns-selected="array_columns_hits_finances"
          name-state-columns-selected="objectColumnsSelectedFinances"
          name-state-columns-selected-initial="objectColumnsSelectedInitialFinances"

          v-bind:filters="filtersHITs"
          name-state-filters="objectFiltersFinances"
          name-local-storage-filters="filtersHITsFinances"
        />
      </base-page-section>

      <base-page-section
        type="table"
        v-bind:identifier="{
          identifier: 'assignments',
          label: 'Assignments'
        }"
      >
        <list-assignments
          name-state-pagination="paginationFinances"
          name-local-storage-pagination="pagination_assignments_finances"

          name-local-storage-columns-selected="array_columns_assignments_finances"
          name-state-columns-selected="objectColumnsSelectedFinances"
          name-state-columns-selected-initial="objectColumnsSelectedInitialFinances"

          v-bind:filters="filtersAssignments"
          name-state-filters="objectFiltersFinances"
          name-local-storage-filters="filtersAssignmentsFinances"
        />
      </base-page-section>
    </base-page>
    <!--    <v-row no-gutters>-->
    <!--      <v-col>-->
    <!--        <v-row dense>-->
    <!--          <v-col-->
    <!--            cols="12"-->
    <!--            class="pt-0"-->
    <!--          >-->
    <!--            <v-list-->
    <!--              dense-->
    <!--              flat-->
    <!--            >-->
    <!--              <v-list-item-group>-->
    <!--                <v-list-item-->
    <!--                  v-for="anchor of arrayAnchors"-->
    <!--                  v-bind:key="anchor.anchor"-->
    <!--                  style="min-height: 24px"-->
    <!--                  v-on:click.native="scrollTo(anchor.anchor)"-->
    <!--                >-->
    <!--                  <v-list-item-icon class="ma-0">-->
    <!--                    <v-icon>mdi-chevron-down</v-icon>-->
    <!--                  </v-list-item-icon>-->
    <!--                  <v-list-item-content class="py-0">-->
    <!--                    {{ anchor.label }}-->
    <!--                  </v-list-item-content>-->
    <!--                </v-list-item>-->
    <!--              </v-list-item-group>-->
    <!--            </v-list>-->
    <!--          </v-col>-->

    <!--          <v-col-->
    <!--            id="finances"-->
    <!--            cols="12"-->
    <!--          >-->
    <!--            <v-row no-gutters>-->
    <!--              <v-col class="mb-2">-->
    <!--                <v-card class="fill-height">-->
    <!--                  <v-card-title>-->
    <!--                    Budget ($)-->
    <!--                  </v-card-title>-->

    <!--                  <v-card-text>-->
    <!--                    <component-show-balance-->
    <!--                      v-bind:expenses="expenses"-->
    <!--                    />-->
    <!--                  </v-card-text>-->
    <!--                </v-card>-->
    <!--              </v-col>-->
    <!--            </v-row>-->
    <!--            <v-row no-gutters>-->
    <!--              <v-col>-->
    <!--                <display-expenses-->
    <!--                  v-bind:expenses="expenses"-->
    <!--                  type-item="batches"-->
    <!--                />-->
    <!--              </v-col>-->
    <!--              <v-col>-->
    <!--                <display-expenses-->
    <!--                  v-bind:expenses="expenses"-->
    <!--                  type-item="hits"-->
    <!--                />-->
    <!--              </v-col>-->
    <!--              <v-col>-->
    <!--                <display-expenses-->
    <!--                  v-bind:expenses="expenses"-->
    <!--                  type-item="assignments"-->
    <!--                />-->
    <!--              </v-col>-->
    <!--            </v-row>-->
    <!--          </v-col>-->

    <!--          <v-col cols="12">-->
    <!--            <v-card-->
    <!--              id="batches"-->
    <!--            >-->
    <!--              <list-batches-->
    <!--                name-state-pagination="paginationFinances"-->
    <!--                name-local-storage-pagination="pagination_batches_finances"-->

    <!--                name-local-storage-columns-selected="array_columns_batches_finances"-->
    <!--                name-state-columns-selected="objectColumnsSelectedFinances"-->
    <!--                name-state-columns-selected-initial="objectColumnsSelectedInitialFinances"-->

    <!--                v-bind:filters="filtersBatches"-->
    <!--                name-state-filters="objectFiltersFinances"-->
    <!--                name-local-storage-filters="filtersBatchesFinances"-->
    <!--              />-->
    <!--            </v-card>-->
    <!--          </v-col>-->

    <!--          <v-col cols="12">-->
    <!--            <v-card-->
    <!--              id="hits"-->
    <!--            >-->
    <!--              <list-hits-->
    <!--                name-state-pagination="paginationFinances"-->
    <!--                name-local-storage-pagination="pagination_hits_finances"-->

    <!--                name-local-storage-columns-selected="array_columns_hits_finances"-->
    <!--                name-state-columns-selected="objectColumnsSelectedFinances"-->
    <!--                name-state-columns-selected-initial="objectColumnsSelectedInitialFinances"-->

    <!--                v-bind:filters="filtersHITs"-->
    <!--                name-state-filters="objectFiltersFinances"-->
    <!--                name-local-storage-filters="filtersHITsFinances"-->
    <!--              />-->
    <!--            </v-card>-->
    <!--          </v-col>-->

    <!--          <v-col cols="12">-->
    <!--            <v-card-->
    <!--              id="assignments"-->
    <!--            >-->
    <!--              <list-assignments-->
    <!--                name-state-pagination="paginationFinances"-->
    <!--                name-local-storage-pagination="pagination_assignments_finances"-->

    <!--                name-local-storage-columns-selected="array_columns_assignments_finances"-->
    <!--                name-state-columns-selected="objectColumnsSelectedFinances"-->
    <!--                name-state-columns-selected-initial="objectColumnsSelectedInitialFinances"-->

    <!--                v-bind:filters="filtersAssignments"-->
    <!--                name-state-filters="objectFiltersFinances"-->
    <!--                name-local-storage-filters="filtersAssignmentsFinances"-->
    <!--              />-->
    <!--            </v-card>-->
    <!--          </v-col>-->
    <!--        </v-row>-->
    <!--      </v-col>-->
    <!--    </v-row>-->
  </div>
</template>

<script>
import {
  mapState, mapMutations, mapActions,
} from 'vuex';

// import ComponentShowBalance from '../../../components/finances/component-show-balance';
import DisplayExpenses from '../../../components/finances/display-expenses';
import ListBatches from '../../../components/batches/list/list-batches';
import { updateSandbox } from '../../../mixins/update-sandbox.mixin';
import ListHits from '../../../components/hits/list/list-hits';
import ListAssignments from '../../../components/assignments/list/list-assignments';
import { ServiceFinances } from '../../../services/finances.service';
import BasePageSection from '../../../components/base/base-page-section';
import BasePage from '../../../components/base/base-page';
import BasePageGroup from '../../../components/base/base-page-group';

export default {
  name: 'AppFinances',
  components: {
    BasePageGroup,
    BasePage,
    BasePageSection,
    ListAssignments,
    ListHits,
    ListBatches,
    // ComponentShowBalance,
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
    arrayAnchors() {
      return [
        {
          label: 'Finances',
          anchor: '#finances',
        },
        {
          label: 'Batches',
          anchor: '#batches',
        },
        {
          label: 'HITs',
          anchor: '#hits',
        },
        {
          label: 'Assignments',
          anchor: '#assignments',
        },
      ];
    },
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
    scrollTo(hash) {
      this.$vuetify.goTo(hash, { offset: 8, duration: 0 });
    },
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
