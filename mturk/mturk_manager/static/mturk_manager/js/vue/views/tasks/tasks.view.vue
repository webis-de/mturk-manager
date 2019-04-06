<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div>
    {{$route.params.id}}
    <router-view></router-view>
    <template
      v-if="$route.params.id === undefined"
    >
      <v-layout>
        <v-flex>
          <h1 class="headline">
            {{ $route.meta.name }}
          </h1>
        </v-flex>
      </v-layout>

      <v-layout>
        <v-flex>
            <!--v-model="indexTab"-->
          <v-tabs
            v-bind:value="$route.meta.index"
            v-on:change="changedView($event)"
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
                    v-bind:function-set-pagination="functionSetPaginationBatches"
                    v-bind:pagination-computed="paginationComputedBatches"
                  >
                    <template v-slot:actions>
                      <component-download-batch></component-download-batch>
                    </template>
                  </list-batches>
                </v-card>
              </v-tab-item>

              <v-tab-item
                key="hits"
              >
                <v-card class="pa-1">
                  <list-hits
                    v-bind:function-set-pagination="functionSetPaginationHITs"
                    v-bind:pagination-computed="paginationComputedHITs"
                  />
                </v-card>
              </v-tab-item>

              <v-tab-item
                key="assignment"
              >
                <v-card class="pa-1">
                  <list-assignments
                    v-bind:function-set-pagination="functionSetPaginationAssignments"
                    v-bind:pagination-computed="paginationComputedAssignments"
                  >
                    <template v-slot:actions>
                      <component-annotate></component-annotate>
                    </template>
                  </list-assignments>
                </v-card>
              </v-tab-item>
            </v-tabs-items>
          </v-tabs>
        </v-flex>
      </v-layout>
    </template>
  </div>
</template>

<script>
import ComponentDownloadBatch from '../../components/batches/component_download_batch';
import ListBatches from '../../components/batches/list/list-batches';
import { mapMutations, mapState } from 'vuex';
import ListHits from '../../components/hits/list/list-hits';
import ListAssignments from '../../components/assignments/list/list-assignments';
import ComponentAnnotate from '../../components/assignments/annotate/component_annotate';

export default {
  name: 'Tasks',
  components: { ComponentAnnotate, ListAssignments, ListHits, ListBatches, ComponentDownloadBatch },
  data() {
    return {
      indexTab: 0,
    };
  },
  computed: {
    ...mapState('moduleBatches', {
      paginationComputedBatches: 'paginationGeneral',
    }),
    ...mapState('moduleHITs', {
      paginationComputedHITs: 'paginationGeneral',
    }),
    ...mapState('moduleAssignments', {
      paginationComputedAssignments: 'paginationGeneral',
    }),
  },
  methods: {
    changedView(index) {
      switch (index) {
        case 0:
          this.$router.push({
            name: 'tasksBatches',
          });
          break;
        case 1:
          this.$router.push({
            name: 'tasksHITs',
          });
          break;
        case 2:
          this.$router.push({
            name: 'tasksAssignments',
          });
          break;
        default:
          break;
      }
    },
    ...mapMutations('moduleBatches', {
      functionSetPaginationBatches: 'setPaginationGeneral',
    }),
    ...mapMutations('moduleHITs', {
      functionSetPaginationHITs: 'setPaginationGeneral',
    }),
    ...mapMutations('moduleAssignments', {
      functionSetPaginationAssignments: 'setPaginationGeneral',
    }),
  },
};
</script>
