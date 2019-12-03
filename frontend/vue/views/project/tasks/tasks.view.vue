<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-row no-gutters>
    <v-col>
      <router-view />
      <template
        v-if="$route.params.id === undefined"
      >
        <v-row dense>
          <v-col
            cols="12"
            class="pt-0"
          >
            <v-list dense flat>
              <v-list-item-group>
                <v-list-item
                  v-for="anchor of arrayAnchors"
                  v-bind:key="anchor.anchor"
                  v-on:click.native="scrollTo(anchor.anchor)"
                  style="min-height: 24px"
                >
                  <v-list-item-icon class="ma-0">
                    <v-icon>mdi-chevron-down</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content class="py-0">
                    {{ anchor.label }}
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-col>

          <v-col cols="12">
            <v-card
              id="batches"
            >
              <list-batches>
                <template v-slot:actions>
                  <component-download-batch />
                </template>
              </list-batches>
            </v-card>
          </v-col>

          <v-col cols="12">
            <v-card
              id="hits"
            >
              <list-hits />
            </v-card>
          </v-col>

          <v-col cols="12">
            <v-card
              id="assignments"
            >
              <list-assignments>
                <template v-slot:actions>
                  <component-annotate />
                </template>
              </list-assignments>
            </v-card>
          </v-col>
        </v-row>

      <!--      <v-row no-gutters>-->
      <!--        <v-col>-->
      <!--          <v-tabs-->
      <!--            v-bind:value="$route.meta.index"-->
      <!--            v-on:change="changedView($event)"-->
      <!--          >-->
      <!--            <v-tab key="batch">-->
      <!--              Batches-->
      <!--            </v-tab>-->
      <!--            <v-tab key="hits">-->
      <!--              HITs-->
      <!--            </v-tab>-->
      <!--            <v-tab key="assignments">-->
      <!--              Assignments-->
      <!--            </v-tab>-->

      <!--            <v-tabs-items-->
      <!--              class="mt-1"-->
      <!--              v-bind:value="$route.meta.index"-->
      <!--            >-->
      <!--              <v-tab-item-->
      <!--                key="batches"-->
      <!--              >-->
      <!--                <v-container-->
      <!--                  fluid-->
      <!--                  class="pa-0"-->
      <!--                >-->
      <!--                  <v-row no-gutters>-->
      <!--                    <v-col xs>-->
      <!--                      <v-card>-->
      <!--                        <list-batches>-->
      <!--                          <template v-slot:actions>-->
      <!--                            <component-download-batch />-->
      <!--                          </template>-->
      <!--                        </list-batches>-->
      <!--                      </v-card>-->
      <!--                    </v-col>-->
      <!--                  </v-row>-->
      <!--                  <v-layout />-->
      <!--                </v-container>-->
      <!--              </v-tab-item>-->

      <!--              <v-tab-item-->
      <!--                key="hits"-->
      <!--              >-->
      <!--                <v-container-->
      <!--                  fluid-->
      <!--                  class="pa-0"-->
      <!--                >-->
      <!--                  <v-row no-gutters>-->
      <!--                    <v-col xs>-->
      <!--                      <v-card>-->
      <!--                        <list-hits />-->
      <!--                      </v-card>-->
      <!--                    </v-col>-->
      <!--                  </v-row>-->
      <!--                  <v-layout />-->
      <!--                </v-container>-->
      <!--              </v-tab-item>-->

      <!--              <v-tab-item-->
      <!--                key="assignment"-->
      <!--              >-->
      <!--                <v-container-->
      <!--                  fluid-->
      <!--                  grid-list-md-->
      <!--                  class="pa-0"-->
      <!--                >-->
      <!--                  <v-row no-gutters>-->
      <!--                    <v-col xs>-->
      <!--                      <v-card>-->
      <!--                        <list-assignments>-->
      <!--                          <template v-slot:actions>-->
      <!--                            <component-annotate />-->
      <!--                          </template>-->
      <!--                        </list-assignments>-->
      <!--                      </v-card>-->
      <!--                    </v-col>-->
      <!--                  </v-row>-->
      <!--                  <v-layout />-->
      <!--                </v-container>-->
      <!--              </v-tab-item>-->
      <!--            </v-tabs-items>-->
      <!--          </v-tabs>-->
      <!--        </v-col>-->
      <!--      </v-row>-->

      <!--      <create-batch />-->
      </template>
    </v-col>
  </v-row>
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
  // mounted() {
  //   console.warn('this.$route', this.$route.hash);
  //   if (this.$route.hash !== '') {
  //     // this.isWaitingForScrolling
  //     // setTimeout(() => {
  //     //   this.$vuetify.goTo(this.$route.hash);
  //     // }, 4000);
  //     // this.$nextTick(() => {
  //     //   this.$vuetify.goTo(this.$route.hash);
  //     // });
  //   }
  // },
  computed: {
    arrayAnchors() {
      return [
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
  },
  methods: {
    onIntersect(entries, observer) {
      // More information about these options
      // is located here: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
      console.warn('entries', entries);
      this.isIntersecting = entries[0].isIntersecting;
    },
    scrollTo(hash) {
      this.$vuetify.goTo(hash, { offset: 8, duration: 0 });
    },
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
