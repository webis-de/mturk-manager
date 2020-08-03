<template>
  <v-dialog
    v-model="dialog"
    max-width="80%"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        class="my-0"
        icon
        x-small
        v-on="on"
      >
        <v-icon color="warning">
          mdi-pencil
        </v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">
          Edit Batch Profile
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
        <v-form
          ref="form"
          lazy-validation
        >
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
          v-on:click="update()"
        >
          Update
        </v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- <v-snackbar
	    v-model="show_snackbar"
	    v-bind:timeout="1500"
	    bottom
	    color="success"
	>
	    Saved!
	    <v-btn
	        text
	        v-on:click="show_snackbar = false"
	    >
	        Close
	    </v-btn>
	</v-snackbar> -->
</template>
<script lang="ts">
import {
  mapActions,
} from 'vuex';
import ComponentFormSettingsBatch from '@/components/settings_project/settings_batch/component_form_settings_batch';
import { settingsBatch } from '@/mixins/settings-batch.mixin';
import validations from '@/mixins/validations.mixin';
import { ServiceSettingsBatch } from '@/modules/settingsBatch/settingsBatch.service';

export default {
  name: 'UpdateSettingsBatch',
  components: {
    ComponentFormSettingsBatch,
  },
  mixins: [validations, settingsBatch],
  props: {
    settingsBatch: {},
  },
  data() {
    return {
      dialog: false,
      disable_unique_name: true,
      name_not_unique: true,
    };
  },
  watch: {
    dialog() {
      this.reset();
    },
  },
  created() {
    this.$v.$touch();
  },
  methods: {
    update() {
      if (this.$refs.form.validate()) {
        this.settings_batch.project = this.$store.getters['moduleProjects/get_project_current'].id;
        ServiceSettingsBatch.update({
          settingsBatch: this.settings_batch,
        });

        this.dialog = false;
        this.$emit('edited');
        this.reset();
      }
    },
    reset() {
      this.update_fields();
      this.$v.$reset();
      this.$v.$touch();
    },
    ...mapActions('moduleProjects', {
      edit_settings_batch: 'edit_settings_batch',
    }),
  },
};
</script>
