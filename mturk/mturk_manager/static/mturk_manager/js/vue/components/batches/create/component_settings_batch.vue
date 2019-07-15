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
      />

      <v-form ref="form">
        <component-form-settings-batch
          v-bind.sync="settings_batch"
          v-bind:v="$v"
          v-bind:validation_errors="validation_errors"
        />
      </v-form>
    </v-flex>
  </v-layout>
</template>

<script>
import _ from 'lodash';
import { settingsBatch } from '../../../mixins/settings-batch.mixin';
import validations from '../../../mixins/validations.mixin';
import ComponentFormSettingsBatch from '../../settings_project/settings_batch/component_form_settings_batch';
import { ServiceSettingsBatch } from '../../../services/service_settings_batch';

export default {
  name: 'ComponentSettingsBatch',
  components: {
    ComponentFormSettingsBatch,
  },
  mixins: [validations, settingsBatch],
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
        if (this.idSettingsBatchCurrent === undefined) {
          this.settingsBatchCurrent = undefined;
          this.update_fields();
          this.$v.$reset();
          this.$store.commit('moduleBatches/setState', {
            objectState: this.settings_batch,
            nameState: 'objectSettingsBatch',
          });
        } else {
          ServiceSettingsBatch.get(this.idSettingsBatchCurrent).then((settingsBatchCurrent) => {
            this.settingsBatchCurrent = settingsBatchCurrent;
            this.update_fields();
            this.$v.$touch();
            this.$store.commit('moduleBatches/setState', {
              objectState: this.settings_batch,
              nameState: 'objectSettingsBatch',
            });
          });
        }
      },
    },
    '$v.$invalid': function (v) {
      this.$emit('updated_is_invalid_settings_batch', v);
    },
  },
  created() {
    this.$store.commit('moduleBatches/setState', {
      objectState: this.settings_batch,
      nameState: 'objectSettingsBatch',
    });

    ServiceSettingsBatch.getAll().then((listSettingsBatch) => {
      this.list_settings_batch = _.orderBy(
        listSettingsBatch,
        settings => settings.name,
      );
    });
  },
  methods: {
    reset() {
      this.idSettingsBatchCurrent = undefined;
    },
  },
};
</script>
