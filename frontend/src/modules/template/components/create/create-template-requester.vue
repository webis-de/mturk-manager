<template>
  <v-dialog
    v-model="dialog"
    fullscreen
  >
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
        <span class="headline">Add Template</span>
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
          <v-select
            v-model="typeTemplate"
            v-bind:items="typesTemplate"
            label="Template Type"
          />

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
            rows="15"
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
import { required, minValue } from 'vuelidate/lib/validators';
import validations from '@/mixins/validations.mixin';
import { TemplateAssignment } from '@/modules/template/templateAssignment.model';
import { TemplateHIT } from '@/modules/template/templateHIT.model';
import { TemplateGlobal } from '@/modules/template/templateGlobal.model';
import { ServiceTemplates } from '@/modules/template/template.service';
import { store } from '@/store/vuex';

export default {
  name: 'CreateTemplateRequester',
  mixins: [validations],
  data() {
    return {
      name: undefined,
      template: undefined,

      dialog: false,

      typesTemplate: [
        { value: 'assignment', text: 'Assignment Template' },
        { value: 'hit', text: 'HIT Template' },
        { value: 'global', text: 'Global Template' },
      ],
      typeTemplate: 'assignment',
    };
  },
  computed: {
    classTemplate() {
      switch (this.typeTemplate) {
        case 'assignment':
          return TemplateAssignment;
        case 'hit':
          return TemplateHIT;
        case 'global':
          return TemplateGlobal;
      }
    },
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
    typeTemplate: {
      required,
    },
  },
  methods: {
    reset() {
      this.name = undefined;
      this.template = undefined;
      this.typeTemplate = 'assignment';
      this.$v.$reset();
    },
    async create() {
      if (this.$refs.form.validate()) {
        const template = new this.classTemplate({
          name: this.name,
          template: this.template,
          project: store.getters['moduleProjects/get_project_current'].id,
        });

        await ServiceTemplates.create({
          template,
        });

        this.dialog = false;
      }
    },
  },
};
</script>
