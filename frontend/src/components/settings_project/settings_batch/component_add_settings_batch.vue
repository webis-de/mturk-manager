<template>
  <div>
    <v-dialog
      v-model="dialog"
      max-width="80%"
    >
      <template v-slot:activator="{ on }">
        <v-btn
          color="primary"
          small
          v-bind:disabled="isDisabled"
          v-on="on"
        >
          <v-icon>mdi-plus</v-icon> Add Profile
        </v-btn>
      </template>

      <v-card>
        <v-card-title>
          <span class="headline">
            Add Batch Profile
          </span>
          <v-spacer />
          <v-btn
            icon
            v-on:click="dialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              required
              v-bind:value="settings_batch.name"
              label="Name"
              v-bind:error-messages="validation_errors.settings_batch.name"
              v-on:input="
                settings_batch.name = $event;
                $v.settings_batch.name.$touch();
              "
            />

            <component-form-settings-batch
              v-bind.sync="settings_batch"
              v-bind:v="$v"
              v-bind:validation_errors="validation_errors"
            />
          </v-form>
          <v-btn
            class="ml-0"
            color="primary"
            v-bind:disabled="$v.$invalid"
            v-on:click="create()"
          >
            Create
          </v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import ComponentFormSettingsBatch from './component_form_settings_batch';
import { settingsBatch } from '../../../mixins/settings-batch.mixin';
import validations from '../../../mixins/validations.mixin';
import { ServiceSettingsBatch } from '../../../services/settings-batch.service';

export default {
  name: 'ComponentAddSettingsBatch',
  components: {
    ComponentFormSettingsBatch,
  },
  mixins: [validations, settingsBatch],
  data() {
    return {
      list_templates_worker: [],
      dialog: false,
    };
  },
  computed: {
    isDisabled() {
      const templatesWorker = this.$store.getters['moduleTemplates/templatesWorker'];
      if (templatesWorker === null) return true;
      return templatesWorker.length === 0;
    },
  },
  watch: {
    dialog() {
      this.reset();
    },
  },
  methods: {
    create() {
      if (this.$refs.form.validate()) {
        ServiceSettingsBatch.create({
          settingsBatch: this.settings_batch,
          project: this.project_current,
        }).then(() => {
          this.dialog = false;
          this.$emit('created');
          this.reset();
        });
      }
    },
    reset() {
      this.update_fields();
      this.$v.$reset();
    },
  },
};
</script>
