<template>
  <v-dialog
    v-model="isCreatingBatch"
    transition="slide-y-transition"
  >
    <!-- persistent -->
    <template v-slot:activator="{ on }">
      <slot v-bind:on="on">
        <v-fab-transition>
          <v-btn
            v-show="!isCreatingBatch"
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
      </slot>
    </template>

    <v-card>
      <v-card-title>
        <span class="headline">
          Create Batch
        </span>
        <v-spacer />
        <v-btn
          icon
          v-on:click="isCreatingBatch = false"
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
                ref="componentUploadCsv"
              />
              <v-divider class="my-3" />

              <v-text-field
                v-model="name"
                required
                label="Name"
              />
              <!-- v-bind:error-messages="validation_errors.name" -->

              <!--              <component-settings-batch-->
              <!--                ref="componentSettingsBatch"-->
              <!--                v-bind:settings-batch="settingsBatch"-->
              <!--                v-on:updated_is_invalid_settings_batch="-->
              <!--                  is_invalid_settings_batch = $event-->
              <!--                "-->
              <!--                v-on:updateSettingsBatch="settingsBatch"-->
              <!--              />-->

              <v-select
                v-model="createBatch.idSettingsBatchSelected"
                v-bind:items="$store.getters['moduleSettingsBatch/settingsBatchSortedByName']"
                label="Batch Profile"
                item-text="name"
                item-value="id"
                clearable
              />

              <v-form ref="form">
                <component-form-settings-batch
                  v-bind.sync="createBatch.settingsBatch"
                  v-bind:v="$v"
                  v-bind:validation_errors="validation_errors"
                />
                <!--                <component-form-settings-batch-->
                <!--                  v-bind.sync="createBatch.settingsBatch"-->
                <!--                />-->
              </v-form>
              <v-divider class="my-3" />
            </v-flex>

            <v-flex xs6>
              <component-overview
                v-bind:settings-batch="createBatch.settingsBatch"
                v-bind:is_invalid_settings_batch="$v.$invalid"
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
                  v-bind:settings-batch="createBatch.settingsBatch"
                  v-bind:is_invalid_settings_batch="$v.$invalid"
                  v-bind:name_batch="name"
                  v-bind:is_creating_batch.sync="isCreatingBatch"
                  v-bind:costs="costs"
                  v-on:is_in_budget="isInBudget = $event"
                />
                <v-flex>
                  <v-btn
                    class="mx-3"
                    text
                    large
                    v-on:click="isCreatingBatch = false"
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

<script lang="ts">
import {
  defineComponent, ref, watch, getCurrentInstance,
} from '@vue/composition-api';

import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';
import ComponentFormSettingsBatch from '@/components/settings_project/settings_batch/component_form_settings_batch.vue';
import { useCreateBatch } from '@/components/batches/create/createBatch';
import { maxValue, minValue, required } from 'vuelidate/lib/validators';
import validations from '@/mixins/validations.mixin';
import ComponentUploadCsv from './component_upload_csv';
import ComponentSettingsBatch from './component_settings_batch';
import SettingsBatchNew from './settings-batch-new';
import ComponentOverview from './component_overview';
import ComponentSubmitBatch from './component_submit_batch';

export default defineComponent({
  name: 'CreateBatch',
  components: {
    ComponentFormSettingsBatch,
    ComponentUploadCsv,
    ComponentSettingsBatch,
    SettingsBatchNew,
    ComponentOverview,
    ComponentSubmitBatch,
  },
  mixins: [validations],
  setup() {
    const instance = getCurrentInstance();

    const isCreatingBatch = ref(false);
    const name = ref<string | undefined>();
    const isInBudget = ref(true);
    const costs = ref();
    const componentSettingsBatch = ref(null);
    const componentUploadCsv = ref(null);

    const createBatch = useCreateBatch(instance);

    watch(isCreatingBatch, () => {
      if (isCreatingBatch.value === false) {
        name.value = undefined;
        createBatch.idSettingsBatchSelected.value = undefined;
        createBatch.settingsBatch.value = new SettingsBatch();
        // componentSettingsBatch.value.reset();
        componentUploadCsv.value.reset();
      }
    });

    return {
      isCreatingBatch,
      name,
      isInBudget,
      costs,
      componentSettingsBatch,
      componentUploadCsv,
      createBatch,
      settings_batch: createBatch.settingsBatch,
    };
  },
  validations() {
    const validations1 = {
      settings_batch: {
        title: {
          required,
        },
        description: {
          required,
        },
        reward: {
          required,
          minValue: minValue(0),
        },
        countAssignments: {
          required,
          minValue: minValue(0),
        },
        countAssignmentsMaxPerWorker: {
          minValue: minValue(0),
        },
        lifetime: {
          required,
          minValue: minValue(0),
        },
        duration: {
          required,
          minValue: minValue(30),
          maxValue: maxValue(31536000),
        },
        templateWorker: {
          required,
        },
        blockWorkers: {
          required,
        },
        keywords: {},
        hasContentAdult: {},
        qualificationAssignmentsApproved: {
          minValue: minValue(0),
          maxValue: maxValue(100),
        },
        qualificationHitsitsApproved: {
          minValue: minValue(0),
        },
        qualificationLocale: {},
      },
    };

    return validations1;
  },
});
</script>

<style scoped></style>
