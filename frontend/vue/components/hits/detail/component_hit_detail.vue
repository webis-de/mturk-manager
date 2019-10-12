<template>
  <v-layout wrap>
    <v-flex>
<!--      <h2 class="headline">-->
<!--        <v-btn-->
<!--          slot="activator"-->
<!--          class="my-0"-->
<!--          icon-->
<!--          small-->
<!--          v-bind:to="{ name: 'tasksHITs' }"-->
<!--        >-->
<!--          <v-icon>mdi-arrow-left</v-icon>-->
<!--        </v-btn>-->
<!--        HIT {{ hit.id_hit }}-->
<!--      </h2>-->
<!--      <v-divider class="my-3" />-->
      <v-container
        fluid
        class="pa-0"
      >
        <v-row dense>
          <v-col class="pt-0">
            <v-card>
              <list-assignments
                v-bind:function-set-pagination="functionSetPagination"
                v-bind:pagination-computed="paginationComputed"

                v-bind:filters="{
                  id_hit: idHit
                }"
              />
            </v-card>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col>
            <v-card>
              <v-card-title
                class="py-1 pointer"
                v-on:click="showBatchProfile = !showBatchProfile"
              >
                <v-row no-gutters>
                  <v-col>
                    Batch profile
                  </v-col>
                  <v-col class="shrink">
                    <v-icon class="foo">
                      {{ showBatchProfile ? 'mdi-chevron-up': 'mdi-chevron-down' }}
                    </v-icon>
                  </v-col>
                </v-row>
              </v-card-title>
              <v-slide-y-transition>
                <v-card-text v-if="showBatchProfile">
                  <component-form-settings-batch
                    v-bind.sync="hit.batch.settings_batch"
                    v-bind:disabled="true"
                  />
                </v-card-text>
              </v-slide-y-transition>
            </v-card>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col>
            <v-card>
              <v-card-title class="py-1">
                Template
              </v-card-title>
              <v-card-text>
                Name: {{ hit.batch.settings_batch.template.name }}<br>
                <sandbox-template v-bind:hit="hit" />
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-flex>
  </v-layout>
</template>
<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';
import ListAssignments from '../../assignments/list/list-assignments';
import { Service_HITs } from '../../../services/service_hits';
import ComponentFormSettingsBatch from '../../settings_project/settings_batch/component_form_settings_batch';
import SandboxTemplate from './sandbox-hit';
import HIT from '../../../classes/hit';

export default {
  name: 'ComponentHitDetail',
  components: {
    SandboxTemplate,
    ComponentFormSettingsBatch,
    ListAssignments,
  },
  // props: {
  //  id_hit: {
  //      required: true,
  //  },
  // },
  props: {
    idHit: {
      required: true,
      type: Number,
    },
  },
  data() {
    return {
      hitIntern: null,
      showBatchProfile: false,
    };
  },
  // watch: {
  //     'worker.is_blocked': function() {
  //         console.log(this.worker.is_blocked)
  //     },
  // },
  computed: {
    hit() {
      console.warn(' this.hitIntern ', this.hitIntern);
      return this.hitIntern === null ? new HIT() : this.hitIntern;
    },
    ...mapGetters('moduleAssignments', {
      array_columns_selected: 'get_array_columns_selected_general',
    }),
    ...mapGetters('moduleHITs', {
      get_object_hits: 'get_object_hits',
    }),
    ...mapGetters(['get_show_progress_indicator']),
    ...mapState('moduleAssignments', {
      paginationComputed: 'paginationGeneral',
    }),
  },
  created() {
    Service_HITs.loadHIT(this.idHit).then((hit) => {
      this.hitIntern = hit;
      this.$store.commit('module_app/setState', {
        nameState: 'nameItem',
        objectState: hit.id_hit,
      });
    });
  },
  methods: {
    ...mapActions('moduleAssignments', {
      function_reset_array_columns: 'reset_array_columns_general',
    }),
    ...mapMutations('moduleAssignments', {
      function_set_array_columns: 'set_array_columns_general',
      functionSetPagination: 'setPaginationGeneral',
    }),
  },
};
</script>

<style lang="scss" scoped>
td {
  height: unset !important;
}
td .v-input--selection-controls {
  padding: unset;
}
.pointer {
  cursor: pointer;
}
  .foo {
    transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
  }
</style>
