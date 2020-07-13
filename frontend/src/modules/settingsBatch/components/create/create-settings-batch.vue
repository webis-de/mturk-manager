<template>
  <v-dialog
    v-model="dialog"
    fullscreen
  >
    <template v-slot:activator="{ on: onDialog }">
      <v-tooltip top>
        <template
          v-slot:activator="{ on: onTooltip }"
          v-bind:disabled="!isDisabled"
        >
          <div v-on="onTooltip">
            <v-btn
              color="primary"
              small
              v-on="onDialog"
            >
              <v-icon>mdi-plus</v-icon> Add profile
            </v-btn>
          </div>
        </template>

        You have to create a worker template.
      </v-tooltip>
    </template>

    <v-card>
      <v-card-title>
        <span class="headline">Add Batch Profile</span>
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
            label="Name"
            v-bind:value="settings_batch.name"
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
      </v-card-text>
      <v-card-actions>
        <v-btn
          text
          class="ml-0"
          color="înfo"
          v-on:click="
            dialog = false;
            reset();
          "
        >
          Cancel
        </v-btn>
        <v-spacer />
        <v-btn
          text
          class="ml-0"
          color="primary"
          v-bind:disabled="$v.$invalid"
          v-on:click="create()"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import validations from '@/mixins/validations.mixin';
import ComponentFormSettingsBatch from '@/components/settings_project/settings_batch/component_form_settings_batch.vue';
import { settingsBatch } from '@/mixins/settings-batch.mixin';
import { ServiceSettingsBatch } from '@/modules/settingsBatch/settingsBatch.service';

export default {
  name: 'CreateSettingsBatch',
  components: { ComponentFormSettingsBatch },
  mixins: [validations, settingsBatch],
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    reset() {
      this.update_fields();
      this.$v.$reset();
    },
    create() {
      if (this.$refs.form.validate()) {
        this.settings_batch.project = this.$store.getters['moduleProjects/get_project_current'].id;

        ServiceSettingsBatch.create({
          settingsBatch: this.settings_batch,
        }).then(() => {
          this.dialog = false;
          this.$emit('created');
          this.reset();
        });
      }
    },
    // async create() {
    //   if (this.$refs.form.validate()) {
    //     const template = new TemplateWorker({
    //       name: this.name,
    //       template: this.template,
    //       project: store.getters['moduleProjects/get_project_current'].id,
    //       heightFrame: this.heightFrame,
    //       templateAssignment: this.idTemplateAssignment === null ? null : this.idTemplateAssignment,
    //       templateHIT: this.idTemplateHIT === null ? null : this.idTemplateHIT,
    //       templateGlobal: this.idTemplateGlobal === null ? null : this.idTemplateGlobal,
    //     });
    //
    //     await ServiceTemplates.create({
    //       template,
    //     });
    //
    //     this.dialog = false;
    //   }
    // },
  },
};
</script>
