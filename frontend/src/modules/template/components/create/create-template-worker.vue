<template>
  <v-dialog
    v-model="dialog"
    fullscreen
  >
    <template #activator="{ on }">
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
        <span class="headline">Add Worker Template</span>
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

          <v-text-field
            type="number"
            required
            v-bind:value="heightFrame"
            label="Frame Height"
            v-bind:error-messages="
              validation_errors.heightFrame
            "
            v-on:input="
              heightFrame = try_number($event);
              $v.heightFrame.$touch();
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

          <v-select
            v-bind:value="idTemplateAssignment"
            v-bind:items="templatesAssignment"
            v-bind:loading="templatesAssignment === null"
            label="Assignment Template"
            item-text="name"
            item-value="id"
            clearable
            v-bind:error-messages="
              validation_errors.idTemplateAssignment
            "
            v-on:input="
              idTemplateAssignment = $event;
              $v.idTemplateAssignment.$touch();
            "
          />

          <v-select
            v-bind:value="idTemplateHIT"
            v-bind:items="templatesHIT"
            v-bind:loading="templatesHIT === null"
            label="HIT Template"
            item-text="name"
            item-value="id"
            clearable
            v-bind:error-messages="
              validation_errors.idTemplateHIT
            "
            v-on:input="
              idTemplateHIT = $event;
              $v.idTemplateHIT.$touch();
            "
          />

          <v-select
            v-bind:value="idTemplateGlobal"
            v-bind:items="templatesGlobal"
            v-bind:loading="templatesGlobal === null"
            label="Global Template"
            item-text="name"
            item-value="id"
            clearable
            v-bind:error-messages="
              validation_errors.idTemplateGlobal
            "
            v-on:input="
              idTemplateGlobal = $event;
              $v.idTemplateGlobal.$touch();
            "
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
import { required, minValue } from 'vuelidate/lib/validators';
import validations from '@/mixins/validations.mixin';
import { ServiceTemplates } from '@/modules/template/template.service';
import { store } from '@/store/vuex';
import helpers from '@/mixins/helpers.mixin';
import { TemplateWorker } from '@/modules/template/templateWorker.model';

export default {
  name: 'CreateTemplateWorker',
  mixins: [helpers, validations],
  data() {
    return {
      name: null,
      heightFrame: 800,
      template: null,
      idTemplateAssignment: null,
      idTemplateHIT: null,
      idTemplateGlobal: null,

      dialog: false,
    };
  },
  computed: {
    templatesAssignment() {
      return this.$store.getters['moduleTemplates/templatesAssignmentSorted'];
    },
    templatesHIT() {
      return this.$store.getters['moduleTemplates/templatesHITSorted'];
    },
    templatesGlobal() {
      return this.$store.getters['moduleTemplates/templatesGlobalSorted'];
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
    heightFrame: {
      required,
    },
    template: {
      required,
    },
    idTemplateAssignment: {},
    idTemplateHIT: {},
    idTemplateGlobal: {},
  },
  methods: {
    reset() {
      this.name = null;
      this.heightFrame = 800;
      this.template = null;
      this.idTemplateAssignment = null;
      this.idTemplateHIT = null;
      this.idTemplateGlobal = null;
      this.$v.$reset();
    },
    async create() {
      if (this.$refs.form.validate()) {
        const template = new TemplateWorker({
          name: this.name,
          template: this.template,
          // @ts-ignore
          project: store.getters['moduleProjects/get_project_current'].id,
          heightFrame: this.heightFrame,
          templateAssignment: this.idTemplateAssignment === null ? null : this.idTemplateAssignment,
          templateHIT: this.idTemplateHIT === null ? null : this.idTemplateHIT,
          templateGlobal: this.idTemplateGlobal === null ? null : this.idTemplateGlobal,
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
