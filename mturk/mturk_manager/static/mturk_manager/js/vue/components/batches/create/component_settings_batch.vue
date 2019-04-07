<template>
  <v-layout wrap>
    <v-flex>
      <!-- {{valid}} -->
      <v-select
        v-model="idSettingsBatchCurrent"
        v-bind:items="list_settings_batch"
        label="Batch Profile"
        item-text="name"
        item-value="id"
        clearable
      ></v-select>

      <v-form ref="form">
        <component-form-settings-batch
          v-bind.sync="settings_batch"
          v-bind:v="$v"
          v-bind:validation_errors="validation_errors"
        ></component-form-settings-batch>
      </v-form>
    </v-flex>
  </v-layout>
</template>

<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';
import { settingsBatch } from '../../../mixins/settings-batch.mixin';
import validations from '../../../mixins/validations.mixin';
import ComponentFormSettingsBatch from '../../settings_project/settings_batch/component_form_settings_batch';
import { ServiceSettingsBatch } from '../../../services/service_settings_batch';

// import ComponentStepUploadCSV from './component_step_upload_csv.vue';
// import ComponentShowMoneySpent from './component-show-money-spent.vue';
// import ComponentShowBatches from './component-show-batches.vue';
export default {
  name: 'ComponentSettingsBatch',
  components: {
    ComponentFormSettingsBatch,
  },
  mixins: [validations, settingsBatch],
  props: {
    // project: {
    //     required: true,
    // },
  },
  data() {
    return {
      idSettingsBatchCurrent: undefined,
      settingsBatchCurrent: undefined,
      name_not_required: true,
      list_settings_batch: [],
    };
  },
  watch: {
    idSettingsBatchCurrent: {
      handler() {
        ServiceSettingsBatch.get(this.idSettingsBatchCurrent).then((settingsBatchCurrent) => {
          this.settingsBatchCurrent = settingsBatchCurrent;
          this.update_fields();
          this.$v.$touch();
          this.$emit('updated_settings_batch', this.settings_batch);
        });
      },
    },
    '$v.$invalid': function (v) {
      this.$emit('updated_is_invalid_settings_batch', v);
    },
  },
  created() {
    this.$emit('updated_settings_batch', this.settings_batch);

    ServiceSettingsBatch.getAll().then((listSettingsBatch) => {
      this.list_settings_batch = _.orderBy(
        listSettingsBatch,
        settings => settings.name,
      );
    });
  },
};
</script>
