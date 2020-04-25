<template>
  <v-dialog
    v-model="dialog"
    max-width="80%"
    persistent
    fullscreen
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
        <span class="headline">Edit Assignment Template</span>
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
            v-bind:value="template_assignment.name"
            v-bind:error-messages="validation_errors.template_assignment.name"
            v-on:input="
              template_assignment.name = $event;
              $v.template_assignment.name.$touch();
            "
          />
          <base-editor
            v-bind:value="template_assignment.template"
            label="Template"
            v-on:input="
              template_assignment.template = $event;
              $v.template_assignment.template.$touch();
            "
          />
          <!--          <v-textarea-->
          <!--            required-->
          <!--            rows="20"-->
          <!--            v-bind:value="template_assignment.template"-->
          <!--            v-on:input="-->
          <!--              template_assignment.template = $event;-->
          <!--              $v.template_assignment.template.$touch();-->
          <!--            "-->
          <!--            label="Template"-->
          <!--            v-bind:error-messages="-->
          <!--              validation_errors.template_assignment.template-->
          <!--            "-->
          <!--          ></v-textarea>-->
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
<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';
import { required, minValue, maxValue } from 'vuelidate/lib/validators';
import helpers from '../../../mixins/helpers.mixin';
import validations from '../../../mixins/validations.mixin';
import Template_Assignment from '../../../classes/template_assignment';
import { ServiceTemplates } from '../../../services/templates.service';
import BaseEditor from '../../../modules/app/components/base-editor';

export default {
  name: 'ComponentEditTemplateAssignment',
  mixins: [helpers, validations],
  props: {
    templateAssignmentCurrent: {},
  },
  data() {
    return {
      template_assignment: new Template_Assignment(
        this.template_assignment_current,
      ),
      dialog: false,
    };
  },
  methods: {
    update(close) {
      if (this.$refs.form.validate()) {
        ServiceTemplates.edit({
          typeTemplate: 'assignment',
          templateCurrent: this.template_assignment_current,
          templateNew: this.template_assignment,
          project: this.project_current,
        }).then(() => {
          ServiceTemplates.cleanup({
            typeTemplate: 'assignmentAll',
            component: this,
            nameEvent: 'edited',
            template: this.template_assignment,
            closeDialog: close === true,
          });
        });
      }
      // console.log(this.project_current);
    },
    reset() {
      this.template_assignment = new Template_Assignment(this.template_assignment_current);
      this.$v.$reset();
      this.$v.$touch();
    },
    ...mapActions('moduleProjects', {
      edit_template_assignment: 'edit_template_assignment',
    }),
  },
  computed: {
    list_templates_assignment() {
      return _.orderBy(
        this.project_current.templates_assignment,
        (template) => template.name,
      );
    },
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  watch: {
    dialog() {
      this.reset();
    },
  },
  validations: {
    template_assignment: {
      name: {
        required,
      },
      template: {
        required,
        contains_form_injection: (value) => value != undefined && value.indexOf(' data-inject_input_forms') >= 0,
      },
    },
  },
  created() {
    this.$v.$touch();
  },
  components: { BaseEditor },
};
</script>
