<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div>
    <router-view />
    <template
      v-if="$route.params.id === undefined"
    >
      <v-layout>
        <v-flex>
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

            <v-tabs-items
              class="mt-1"
              v-bind:value="$route.meta.index"
            >
              <v-tab-item
                key="batches"
              >
                <v-container
                  fluid
                  grid-list-md
                  class="pa-0"
                >
                  <v-layout wrap>
                    <v-flex xs>
                      <v-card class="pa-1">
                        <list-batches>
                          <template v-slot:actions>
                            <component-download-batch />
                          </template>
                        </list-batches>
                      </v-card>
                    </v-flex>
                  </v-layout>
                  <v-layout />
                </v-container>
              </v-tab-item>

              <v-tab-item
                key="hits"
              >
                <v-container
                  fluid
                  grid-list-md
                  class="pa-0"
                >
                  <v-layout wrap>
                    <v-flex xs>
                      <v-card class="pa-1">
                        <list-hits />
                      </v-card>
                    </v-flex>
                  </v-layout>
                  <v-layout />
                </v-container>
              </v-tab-item>

              <v-tab-item
                key="assignment"
              >
                <v-container
                  fluid
                  grid-list-md
                  class="pa-0"
                >
                  <v-layout wrap>
                    <v-flex xs>
                      <v-card class="pa-1">
                        <list-assignments>
                          <template v-slot:actions>
                            <component-annotate />
                          </template>
                        </list-assignments>
                      </v-card>
                    </v-flex>
                  </v-layout>
                  <v-layout />
                </v-container>
              </v-tab-item>
            </v-tabs-items>
          </v-tabs>
        </v-flex>
      </v-layout>

      <create-batch />
    </template>
  </div>
</template>

<script>
import ComponentDownloadBatch from '../../../components/batches/component_download_batch';
import ListBatches from '../../../components/batches/list/list-batches';
import ListHits from '../../../components/hits/list/list-hits';
import ListAssignments from '../../../components/assignments/list/list-assignments';
import ComponentAnnotate from '../../../components/assignments/annotate/component_annotate';
import CreateBatch from '../../../components/batches/create/component_create_batch';

export default {
  name: 'Tasks',
  components: {
    CreateBatch,
    ComponentAnnotate,
    ListAssignments,
    ListHits,
    ListBatches,
    ComponentDownloadBatch,
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
  },
};
</script>
