<template>
  <v-dialog
    v-model="dialog"
    max-width="80%"
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
        <span class="headline">Edit {{ labelTypeTemplate }} Template</span>
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

          <template-assignment-sandbox
            v-if="templateInternal.type === 'assignment'"

            v-model="templateInternal.template"
            label="Template"
            v-on:input="processInput($event)"
          />

          <v-textarea
            v-else

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
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-btn
          text
          class="ml-0"
          color="înfo"
          v-bind:disabled="$v.$invalid"
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
import { TemplateBase } from '@/modules/template/templateBase.model';
import cloneDeep from 'lodash-es/cloneDeep';
import { mapActions, mapGetters } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import helpers from '@/mixins/helpers.mixin';
import validations from '@/mixins/validations.mixin';
import TemplateAssignmentSandbox from '@/modules/template/components/sandbox/template-assignment-sandbox.vue';
import debounce from 'lodash-es/debounce';
import { ServiceTemplates } from '@/modules/template/template.service';

export default {
  name: 'UpdateTemplateRequester',
  components: { TemplateAssignmentSandbox },
  mixins: [helpers, validations],
  props: {
    template: {
      required: true,
      type: TemplateBase,
    },
  },
  data() {
    return {
      templateInternal: cloneDeep(this.template),
      dialog: false,
    };
  },
  computed: {
    labelTypeTemplate() {
      switch (this.templateInternal.type) {
        case 'assignment':
          return 'Assignment';
        case 'hit':
          return 'HIT';
        case 'global':
          return 'Global';
        default:
          return 'Requester';
      }
    },
    isActiveAutosave() {
      return this.$store.state.module_app.isActiveAutosave;
    },
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
    reset() {
      this.templateInternal = cloneDeep(this.template);
      this.$v.$reset();
      this.$v.$touch();
    },
  },
  watch: {
    dialog() {
      this.reset();
    },
  },
  validations: {
    templateInternal: {
      name: {
        required,
      },
      template: {
        required,
        // TODO constraints depending on template type
        // contains_form_injection: (value) => value != undefined && value.indexOf(' data-inject_input_forms') >= 0,
      },
    },
  },
  created() {
    this.$v.$touch();
  },
};
</script>

<style scoped>

</style>
