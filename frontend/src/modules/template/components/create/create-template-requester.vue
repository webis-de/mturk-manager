<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on }">
      <v-btn
        color="primary"
        small
        v-on="on"
      >
        <v-icon>mdi-plus</v-icon> Add Template
      </v-btn>
    </template>

    <v-card>
      <v-card-title>
        <span class="headline">Add Assignment Template</span>
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
            v-bind:value="name"
            v-bind:error-messages="validation_errors.name"
            v-on:input="
              name = $event;
              $v.name.$touch();
            "
          />
          <v-textarea
            required
            rows="20"
            v-bind:value="template"
            label="Template"
            v-bind:error-messages="validation_errors.template"
            v-on:input="
              template = $event;
              $v.template.$touch();
            "
          />

          <!-- <component-form-settings-batch
			        	v-bind.sync="settings_batch"
			        ></component-form-settings-batch> -->
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
</template>

<script lang="ts">
import { required, minValue } from 'vuelidate/lib/validators';
import validations from '@/mixins/validations.mixin';

export default {
  name: 'CreateTemplateRequester',
  mixins: [validations],
  data() {
    return {
      name: undefined,
      template: undefined,

      dialog: false,
    };
  },
  watch: {
    dialog() {
      this.reset();
    },
  },
  validations: {
    name: {
      required,
    },
    template: {
      required,
      // TODO constraints depending on template type
      // contains_form_injection: (value) => value != undefined && value.indexOf(' data-inject_input_forms') >= 0,
    },
  },
  methods: {
    reset() {
      this.name = undefined;
      this.template = undefined;
      this.$v.$reset();
    },
    create() {
      if (this.$refs.form.validate()) {
        console.warn(this.template, 'this.template');
        // ServiceTemplates.create({
        //   typeTemplate: 'assignment',
        //   template: {
        //     name: this.name,
        //     template: this.template,
        //   },
        //   project: this.project_current,
        // });
      }
    },
  },
};
</script>
