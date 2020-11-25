<template>
  <v-layout wrap>
    <v-flex>
      <!-- {{valid}} -->
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
      </v-form>
    </v-flex>
  </v-layout>
</template>

<script>
import { defineComponent } from '@vue/composition-api';
import { useCreateBatch } from '@/components/batches/create/createBatch';
import { maxValue, minValue, required } from 'vuelidate/lib/validators';
import _ from 'lodash';
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';
import { settingsBatch } from '../../../mixins/settings-batch.mixin';
import validations from '../../../mixins/validations.mixin';
import ComponentFormSettingsBatch from '../../settings_project/settings_batch/component_form_settings_batch';

export default defineComponent({
  name: 'SettingsBatchNew',
  components: {
    ComponentFormSettingsBatch,
  },
  props: {
    name: {
      required: true,
      type: String,
    },
  },
  setup(props) {
    const createBatch = useCreateBatch();
    console.warn(props.settingsBatch, 'props.settingsBatch');

    return {
      createBatch,
    };
  },
  mixins: [validations],
  // mixins: [validations, settingsBatch],
  data() {
    return {
      idSettingsBatchCurrent: undefined,
      settingsBatchCurrent: undefined,
      name_not_required: true,
    };
  },
  watch: {
    settings_batch: {
      handler() {
        this.$store.commit('moduleBatches/setState', {
          objectState: this.settings_batch,
          nameState: 'objectSettingsBatch',
        });
      },
      deep: true,
    },
    idSettingsBatchCurrent: {
      handler() {
        if (this.idSettingsBatchCurrent === undefined) {
          this.settingsBatchCurrent = undefined;
          this.update_fields();
          this.$v.$reset();
          this.$store.commit('moduleBatches/setState', {
            objectState: this.settings_batch,
            nameState: 'objectSettingsBatch',
          });
        } else {
          this.settingsBatchCurrent = this.$store.state.moduleSettingsBatch.settingsBatch[this.idSettingsBatchCurrent];
          this.update_fields();
          this.$v.$touch();
          this.$store.commit('moduleBatches/setState', {
            objectState: this.settings_batch,
            nameState: 'objectSettingsBatch',
          });
        }
      },
    },
    '$v.$invalid': {
      handler(v) {
        this.$emit('updated_is_invalid_settings_batch', v);
      },
    },
  },
  // created() {
  //   this.$store.commit('moduleBatches/setState', {
  //     objectState: this.settings_batch,
  //     nameState: 'objectSettingsBatch',
  //   });
  // },
  methods: {
    reset() {
      this.idSettingsBatchCurrent = undefined;
    },
  },
  validations() {
    const validations = {
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

    return validations;
  },
});
</script>
