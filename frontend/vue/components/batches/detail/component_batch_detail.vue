<template>
  <v-row no-gutters>
    <v-col>
<!--      <h2 class="headline">-->
<!--        <v-btn-->
<!--          slot="activator"-->
<!--          class="my-0"-->
<!--          icon-->
<!--          small-->
<!--          v-bind:to="{ name: 'tasksBatches' }"-->
<!--        >-->
<!--          <v-icon>mdi-arrow-left</v-icon>-->
<!--        </v-btn>-->
<!--        Batch {{ batch.name }}-->
<!--      </h2>-->
<!--      <v-divider class="my-3" />-->
      <v-container
        fluid
        class="pa-0"
      >
        <v-row dense>
          <v-col class="pt-0">
            <v-card>
              <list-hits
                v-bind:pagination-computed="paginationComputed"
                v-bind:function-set-pagination="functionSetPagination"

                v-bind:filters="{
                  id_batch: idBatch
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
                    v-bind.sync="batch.settings_batch"
                    v-bind:disabled="true"
                  />
                </v-card-text>
              </v-slide-y-transition>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-col>
  </v-row>
</template>
<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import { Service_Batches } from '../../../services/service_batches';
import ListHits from '../../hits/list/list-hits';
import ComponentFormSettingsBatch from '../../settings_project/settings_batch/component_form_settings_batch';

export default {
  name: 'ComponentBatchDetail',
  components: {
    ComponentFormSettingsBatch,
    ListHits,
  },
  props: {
    idBatch: {
      required: true,
      type: Number,
    },
  },
  data() {
    return {
      batch_intern: undefined,
      showBatchProfile: false,
    };
  },
  // watch: {
  //     'worker.is_blocked': function() {
  //         console.log(this.worker.is_blocked)
  //     },
  // },
  computed: {
    // list_hits() {
    //     if(this.batch.object_hits == undefined)
    //     {
    //         return [];
    //     } else {
    //         return _.orderBy(this.batch.object_hits);
    //     }
    // },
    batch() {
      return this.batch_intern === undefined ? {} : this.batch_intern;
    },

    // status_block() {
    //     if(this.worker.is_blocked == undefined)
    //     {
    //         return {
    //             description: 'Loading',
    //             color: 'success',
    //             icon: '',
    //         };
    //     }

    //     switch(this.worker.is_blocked)
    //     {
    //         case STATUS_BLOCK.NONE:
    //             return {
    //                 description: 'Not Blocked',
    //                 color: 'success',
    //                 icon: 'check',
    //             };
    //         case STATUS_BLOCK.SOFT:
    //             return {
    //                 description: 'Soft Blocked',
    //                 color: 'warning',
    //                 icon: 'block',
    //             };
    //         case STATUS_BLOCK.HARD:
    //             return {
    //                 description: 'Hard Blocked',
    //                 color: 'error',
    //                 icon: 'block',
    //             };
    //     }
    // },
    // ...mapGetters('moduleBatches', {
    //     'get_object_batches': 'get_object_batches',
    // }),
    ...mapGetters('moduleHITs', {
      array_columns_selected: 'get_array_columns_selected_general',
    }),
    ...mapGetters(['get_show_progress_indicator']),
    ...mapState('moduleHITs', {
      paginationComputed: 'paginationGeneral',
    }),
  },
  created() {
    Service_Batches.get_batch(this.idBatch).then((batch) => {
      this.batch_intern = batch;
      this.$store.commit('module_app/setState', {
        nameState: 'nameItem',
        objectState: batch.name,
      });
    });
  },
  methods: {
    ...mapActions('moduleHITs', {
      function_reset_array_columns: 'reset_array_columns_general',
    }),
    ...mapMutations('moduleHITs', {
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
</style>
