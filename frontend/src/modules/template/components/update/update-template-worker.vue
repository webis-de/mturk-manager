<template>
  <v-dialog
    v-model="dialog"
    fullscreen
  >
    <template v-slot:activator="{ on }">
      <slot name="activator">
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
      </slot>
    </template>

    <v-card>
      <v-card-title>
        <span class="headline">Edit worker template</span>
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
            label="Name"
            v-bind:value="templateInternal.name"
            v-bind:error-messages="validation_errors.templateInternal.name"
            dense
            v-on:input="
              templateInternal.name = $event;
              $v.templateInternal.name.$touch();
            "
          />

          <v-text-field
            type="number"
            required
            v-bind:value="templateInternal.heightFrame"
            label="Frame Height"
            v-bind:error-messages="
              validation_errors.templateInternal.heightFrame
            "
            v-on:input="
              templateInternal.heightFrame = try_number($event);
              $v.templateInternal.heightFrame.$touch();
            "
          />

          <v-textarea
            required
            rows="20"
            v-bind:value="templateInternal.template"
            label="Template"
            v-bind:error-messages="
              validation_errors.templateInternal.template
            "
            v-on:input="
              templateInternal.template = $event;
              $v.templateInternal.template.$touch();
            "
          />

          <v-select
            v-bind:value="templateInternal.templateAssignment"
            v-bind:items="templatesAssignment"
            v-bind:loading="templatesAssignment === null"
            label="Assignment Template"
            item-text="name"
            item-value="id"
            clearable
            v-bind:error-messages="
              validation_errors.templateInternal.templateAssignment
            "
            v-on:input="
              templateInternal.templateAssignment = $event;
              $v.templateInternal.templateAssignment.$touch();
            "
          />

          <v-select
            v-bind:value="templateInternal.templateHIT"
            v-bind:items="templatesHIT"
            v-bind:loading="templatesHIT === null"
            label="HIT Template"
            item-text="name"
            item-value="id"
            clearable
            v-bind:error-messages="
              validation_errors.templateInternal.templateHIT
            "
            v-on:input="
              templateInternal.templateHIT = $event;
              $v.templateInternal.templateHIT.$touch();
            "
          />

          <v-select
            v-bind:value="templateInternal.templateGlobal"
            v-bind:items="templatesGlobal"
            v-bind:loading="templatesGlobal === null"
            label="Global Template"
            item-text="name"
            item-value="id"
            clearable
            v-bind:error-messages="
              validation_errors.templateInternal.templateGlobal
            "
            v-on:input="
              templateInternal.templateGlobal = $event;
              $v.templateInternal.templateGlobal.$touch();
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
          v-on:click="update()"
        >
          Save
        </v-btn>

        <v-btn
          text
          class="ml-0"
          color="success"
          v-bind:disabled="$v.$invalid"
          v-on:click="update(true)"
        >
          Save and Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import cloneDeep from 'lodash-es/cloneDeep';
import { required } from 'vuelidate/lib/validators';
import helpers from '@/mixins/helpers.mixin';
import validations from '@/mixins/validations.mixin';
import TemplateAssignmentSandbox from '@/modules/template/components/sandbox/template-assignment-sandbox.vue';
import debounce from 'lodash-es/debounce';
import { ServiceTemplates } from '@/modules/template/template.service';
import { TemplateWorker } from '@/modules/template/templateWorker.model';

export default {
  name: 'UpdateTemplateWorker',
  components: { TemplateAssignmentSandbox },
  mixins: [helpers, validations],
  props: {
    template: {
      required: true,
      type: TemplateWorker,
    },
  },
  data() {
    return {
      templateInternal: cloneDeep(this.template),
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
    isActiveAutosave() {
      return this.$store.state.module_app.isActiveAutosave;
    },
  },
  created() {
    this.$v.$touch();
  },
  methods: {
    processInput(value) {
      this.templateInternal.template = value;
      this.$v.templateInternal.template.$touch();

      if (this.$v.$invalid === false && this.isActiveAutosave === true) {
        this.saveDebounced();
      }
    },
    saveDebounced: debounce(function () {
      this.update();
    }, 500),
    update(close = false) {
      console.warn(this.templateInternal, 'this.templateInternal');
      if (this.$refs.form.validate()) {
        ServiceTemplates.update({
          templateCurrent: this.template,
          templateNew: this.templateInternal,
        }).then(() => {
          if (close) this.dialog = false;
          // ServiceTemplates.cleanup({
          //   typeTemplate: 'assignment',
          //   component: this,
          //   nameEvent: 'edited',
          //   template: this.templateInternal,
          //   closeDialog: close === true,
          // });
        });
      }
      // console.log(this.project_current);
    },
    watch: {
      'templateInternal.templateAssignment': function (value) {
        if (value === undefined) this.templateInternal.templateAssignment = null;
      },
      'templateInternal.templateHIT': function (value) {
        if (value === undefined) this.templateInternal.templateHIT = null;
      },
      'templateInternal.templateGlobal': function (value) {
        if (value === undefined) this.templateInternal.templateGlobal = null;
      },
      dialog() {
        this.reset();
      },
    },
    reset() {
      this.templateInternal = cloneDeep(this.template);
      this.$v.$reset();
      this.$v.$touch();
    },
  },
  validations: {
    templateInternal: {
      name: {
        required,
      },
      heightFrame: {
        required,
      },
      template: {
        required,
        // TODO constraints depending on template type
        // contains_form_injection: (value) => value != undefined && value.indexOf(' data-inject_input_forms') >= 0,
      },
      templateAssignment: {},
      templateHIT: {},
      templateGlobal: {},
    },
  },
};
</script>

<style scoped>

</style>
