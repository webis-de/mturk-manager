<template>
  <v-dialog
    v-model="is_creating_batch"
    transition="slide-y-transition"
  >
    <!-- persistent -->
    <v-fab-transition slot="activator">
      <v-btn
        v-show="!is_creating_batch"
        color="pink"
        fab
        left
        bottom
        fixed
        large
      >
        <v-icon>add</v-icon>
      </v-btn>
    </v-fab-transition>

    <v-card>
      <v-card-title>
        <span class="headline">
          Create Batch
        </span>
        <v-spacer />
        <v-btn
          icon
          v-on:click="is_creating_batch = false"
        >
          <v-icon>close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-container class="mx-0">
          <v-layout
            row
            wrap
          >
            <v-flex xs6>
              <component-upload-csv
                ref="component_upload_csv"
              />
              <v-divider class="my-3" />

              <v-text-field
                required
                v-bind:value="name"
                label="Name"
                v-on:input="
                  name = $event;
                  $v.name.$touch();
                "
              />
              <!-- v-bind:error-messages="validation_errors.name" -->

              <component-settings-batch
                ref="component_settings_batch"
                v-on:updated_settings_batch="settings_batch_current = $event"
                v-on:updated_is_invalid_settings_batch="
                  is_invalid_settings_batch = $event
                "
              />
              <v-divider class="my-3" />
            </v-flex>

            <v-flex xs6>
              <component-overview
                v-bind:settings_batch_current="settings_batch_current"
                v-bind:is_invalid_settings_batch="is_invalid_settings_batch"
                v-on:updated_costs_with_fee="costs = $event"
              />

              <v-layout>
                <v-flex shrink>
                  <v-alert
                    class="ml-3"
                    type="error"
                    v-bind:value="isInBudget === false"
                  >
                    This batch exceeds your budget!
                  </v-alert>
                </v-flex>
              </v-layout>
              <v-layout wrap>

                <!-- v-if="is_valid_csv" -->
                <component-submit-batch
                  class="shrink"
                  v-bind:settings_batch_current="settings_batch_current"
                  v-bind:is_invalid_settings_batch="is_invalid_settings_batch"
                  v-bind:name_batch="name"
                  v-bind:is_creating_batch.sync="is_creating_batch"
                  v-bind:costs="costs"
                  v-on:is_in_budget="isInBudget = $event"
                />
                <v-flex>
                  <v-btn
                    class="mx-3"
                    flat
                    large
                    v-on:click="is_creating_batch = false"
                  >
                    Cancel
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import validations from '../../../mixins/validations';

import ComponentUploadCsv from './component_upload_csv.vue';
import ComponentSettingsBatch from './component_settings_batch.vue';
import ComponentOverview from './component_overview.vue';
import ComponentSubmitBatch from './component_submit_batch.vue';
// import ComponentStepSettings from './component_step_settings.vue';
// import ComponentStepOverview from './component_step_overview.vue';
// import ComponentShowMoneySpent from './component-show-money-spent.vue';
// import ComponentShowBatches from './component-show-batches.vue';
export default {
  name: 'ComponentCreateBatch',
  mixins: [validations],
  data() {
    return {
      is_creating_batch: false,

      name: undefined,
      settings_batch_current: undefined,
      is_invalid_settings_batch: true,

      isInBudget: true,
      costs: undefined,
    };
  },
  watch: {
    is_creating_batch() {
      if (this.is_creating_batch === false) {
        this.$refs.component_settings_batch.update_fields();
        this.$refs.component_upload_csv.reset();
      }
    },
  },
  methods: {
    // cancel() {
    //     this.is_creating_batch = false;
    //     this.number_step_current = 1;
    //     this.data_csv = undefined;
    //     this.$refs[1][0].reset()
    // },
    // next() {
    //     this.number_step_current += 1;
    // },
    // back() {
    //     this.number_step_current -= 1;
    // },
    //     refresh_data() {
    //         this.set_show_progress_indicator(true);
    //         this.set_show_progress_indicator(true);
    //         this.sync_database().then(() => {
    //             this.set_show_progress_indicator(false);
    //         });
    //         this.update_balance().then(() => {
    //             this.set_show_progress_indicator(false);
    //         });
    //     },
    //     ...mapActions(['set_show_progress_indicator']),
    //     ...mapActions('moduleBatches', {
    //         'sync_database': 'sync_database',
    //     }),
    //     ...mapActions('moduleMoney', {
    //         'update_balance': 'update_balance'
    //     }),
    // },
    // watch: {
    //     use_sandbox: function() {
    //         this.refresh_data();
    //     },
  },
  computed: {
    // count_hits() {
    //     if(this.is_valid_csv)
    //     {
    //         return this.data_csv.length;
    //     }
    //     return null;
    // },
    // name_file() {
    //     if(this.file_csv != null)
    //     {
    //         return this.file_csv.name;
    //     }
    //     return null;
    // },
    // get_variables() {
    //     if(this.is_valid_csv)
    //     {
    //         return Object.keys(this.data_csv[0]);
    //     }

    //     return [];
    // },
    // data_csv() {
    //     if(this.is_valid_csv)
    //     {
    //         return this.object_csv_parsed.data;
    //     }
    //     return null;
    // },
    // is_valid_csv() {
    //     if(this.object_csv_parsed == undefined)
    //     {
    //         return false;
    //     } else {
    //         return this.object_csv_parsed.errors.length == 0;
    //     }
    // },
    // step_current: function() {
    //     return this.list_steps[this.number_step_current - 1];
    // },
    //     ...mapState('module_app', ['use_sandbox']),
    ...mapGetters('moduleBatches', {
      // 'get_object_csv_parsed': 'get_object_csv_parsed',
      is_valid_csv: 'is_valid_csv',
    }),
  },
  validations: {
    name: {
      // required
    },
  },
  // created: function() {
  //     this.refresh_data();
  // },

  components: {
    ComponentUploadCsv,
    ComponentSettingsBatch,
    ComponentOverview,
    ComponentSubmitBatch,
  },
};
</script>

<style scoped></style>
