<template>
  <v-dialog
    v-model="is_creating_batch"
    transition="slide-y-transition"
  >
    <!-- persistent -->
    <template v-slot:activator="{ on }">
      <v-fab-transition>
        <v-btn
          v-show="!is_creating_batch"
          color="primary"
          fab
          right
          bottom
          fixed
          large
          v-on="on"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-fab-transition>
    </template>

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
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-container class="mx-0">
          <v-layout
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
                v-on:updated_is_invalid_settings_batch="
                  is_invalid_settings_batch = $event
                "
              />
              <v-divider class="my-3" />
            </v-flex>

            <v-flex xs6>
              <component-overview
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
                <component-submit-batch
                  class="shrink"
                  v-bind:is_invalid_settings_batch="is_invalid_settings_batch"
                  v-bind:name_batch="name"
                  v-bind:is_creating_batch.sync="is_creating_batch"
                  v-bind:costs="costs"
                  v-on:is_in_budget="isInBudget = $event"
                />
                <v-flex>
                  <v-btn
                    class="mx-3"
                    text
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
import validations from '../../../mixins/validations.mixin';

import ComponentUploadCsv from './component_upload_csv';
import ComponentSettingsBatch from './component_settings_batch';
import ComponentOverview from './component_overview';
import ComponentSubmitBatch from './component_submit_batch';

export default {
  name: 'CreateBatch',
  components: {
    ComponentUploadCsv,
    ComponentSettingsBatch,
    ComponentOverview,
    ComponentSubmitBatch,
  },
  mixins: [validations],
  data() {
    return {
      is_creating_batch: false,

      name: undefined,
      is_invalid_settings_batch: true,

      isInBudget: true,
      costs: undefined,
    };
  },
  watch: {
    is_creating_batch() {
      if (this.is_creating_batch === false) {
        this.name = undefined;
        this.$refs.component_settings_batch.reset();
        this.$refs.component_upload_csv.reset();
      }
    },
  },
  validations: {
    name: {
      // required
    },
  },
};
</script>

<style scoped></style>
