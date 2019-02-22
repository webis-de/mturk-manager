<template>
  <v-layout wrap>
    <v-flex>
      <!-- {{valid}} -->
      <v-select
        v-model="settingsBatchCurrent"
        v-bind:items="list_settings_batch"
        label="Batch Profile"
        item-text="name"
        item-value="id"
        return-object
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
import settings_batch from '../../../mixins/settings_batch';
import validations from '../../../mixins/validations';
import ComponentFormSettingsBatch from '../../settings_project/settings_batch/component_form_settings_batch';

// import ComponentStepUploadCSV from './component_step_upload_csv.vue';
// import ComponentShowMoneySpent from './component-show-money-spent.vue';
// import ComponentShowBatches from './component-show-batches.vue';
export default {
  mixins: [validations, settings_batch],
  name: 'component-settings-batch',
  props: {
    // project: {
    //     required: true,
    // },
  },
  data() {
    return {
      settingsBatchCurrent: undefined,
      name_not_required: true,
    };
  },
  methods: {},
  computed: {
    list_settings_batch() {
      if (this.project_current.settings_batch == null) return [];
      return _.orderBy(
        this.project_current.settings_batch,
        settings => settings.name,
      );
    },
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  watch: {
    settingsBatchCurrent: {
      handler() {
        this.update_fields();
        this.$v.$touch();
        this.$emit('updated_settings_batch', this.settings_batch);
        // this.$emit('updated_settings_batch', this.settings_batch_current);
      },
      // deep: true,
    },
    '$v.$invalid': function (v) {
      this.$emit('updated_is_invalid_settings_batch', v);
    },
  },
  created() {
    this.$emit('updated_settings_batch', this.settings_batch);
  },
  mounted() {},
  components: {
    ComponentFormSettingsBatch,
  },
};
</script>
