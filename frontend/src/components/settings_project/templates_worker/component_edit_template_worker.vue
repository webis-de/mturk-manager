<template>
  <v-dialog
    v-model="dialog"
    max-width="80%"
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
        <span class="headline">Edit Worker Template</span>
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
            v-bind:value="template_worker.name"
            v-bind:error-messages="validation_errors.template_worker.name"
            v-on:input="
              template_worker.name = $event;
              $v.template_worker.name.$touch();
            "
          />
          <v-text-field
            type="number"
            required
            v-bind:value="template_worker.height_frame"
            label="Height"
            v-bind:error-messages="
              validation_errors.template_worker.height_frame
            "
            v-on:input="
              template_worker.height_frame = try_number($event);
              $v.template_worker.height_frame.$touch();
            "
          />

          <base-editor
            v-model="template_worker.template"
            v-bind:label="'Template'"
          />

          <!--          <v-textarea-->
          <!--            required-->
          <!--            rows="20"-->
          <!--            v-bind:value="template_worker.template"-->
          <!--            label="Template"-->
          <!--            v-bind:error-messages="validation_errors.template_worker.template"-->
          <!--            v-on:input="-->
          <!--              template_worker.template = $event;-->
          <!--              $v.template_worker.template.$touch();-->
          <!--            "-->
          <!--          />-->

          <v-select
            v-bind:value="template_worker.template_assignment"
            v-bind:items="arrayTemplatesAssignment"
            label="Assignment Template"
            item-text="name"
            item-value="id"
            v-bind:error-messages="
              validation_errors.template_worker.template_assignment
            "
            clearable
            v-on:input="
              template_worker.template_assignment = $event;
              $v.template_worker.template_assignment.$touch();
            "
          />

          <v-select
            v-bind:value="template_worker.template_hit"
            v-bind:items="arrayTemplatesHIT"
            label="HIT Template"
            item-text="name"
            item-value="id"
            v-bind:error-messages="
              validation_errors.template_worker.template_hit
            "
            clearable
            v-on:input="
              template_worker.template_hit = $event;
              $v.template_worker.template_hit.$touch();
            "
          />

          <v-select
            v-bind:value="template_worker.template_global"
            v-bind:items="arrayTemplatesGlobal"
            label="Global Template"
            item-text="name"
            item-value="id"
            v-bind:error-messages="
              validation_errors.template_worker.template_global
            "
            clearable
            v-on:input="
              template_worker.template_global = $event;
              $v.template_worker.template_global.$touch();
            "
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
<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';
import { required, minValue, maxValue } from 'vuelidate/lib/validators';
import helpers from '../../../mixins/helpers.mixin';
import validations from '../../../mixins/validations.mixin';
import Template_Worker from '../../../classes/template_worker';
import { ServiceTemplates } from '../../../services/service_templates';
import BaseEditor from '../../../modules/app/components/base-editor';

export default {
  name: 'ComponentEditTemplateWorker',
  mixins: [helpers, validations],
  props: {
    templateWorkerCurrent: {},
  },
  data() {
    return {
      template_worker: new Template_Worker(this.templateWorkerCurrent),
      dialog: false,
    };
  },
  methods: {
    update() {
      if (this.$refs.form.validate()) {
        ServiceTemplates.edit({
          typeTemplate: 'worker',
          templateCurrent: this.templateWorkerCurrent,
          templateNew: this.template_worker,
          project: this.project_current,
        }).then(() => {
          ServiceTemplates.cleanup({
            typeTemplate: 'workerAll',
            component: this,
            nameEvent: 'edited',
            template: this.template_worker,
          });
        });
      }
      // console.log(this.project_current);
    },
    reset() {
      (this.template_worker = new Template_Worker(
        this.templateWorkerCurrent,
      )),
      this.$v.$reset();
      this.$v.$touch();
    },
    ...mapActions('moduleProjects', {
      edit_template_worker: 'edit_template_worker',
    }),
  },
  computed: {
    arrayTemplatesAssignment() {
      if (this.arrayTemplatesAssignmentAll === null) {
        return [];
      }

      return _.orderBy(
        this.arrayTemplatesAssignmentAll,
        (template) => template.name,
      );
    },
    arrayTemplatesHIT() {
      if (this.arrayTemplatesHITAll === null) {
        return [];
      }

      return _.orderBy(
        this.arrayTemplatesHITAll,
        (template) => template.name,
      );
    },
    arrayTemplatesGlobal() {
      if (this.arrayTemplatesGlobalAll === null) {
        return [];
      }

      return _.orderBy(
        this.arrayTemplatesGlobalAll,
        (template) => template.name,
      );
    },
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
    ...mapState('moduleTemplates', {
      arrayTemplatesAssignmentAll: 'arrayItemsAssignmentAll',
      arrayTemplatesHITAll: 'arrayItemsHITAll',
      arrayTemplatesGlobalAll: 'arrayItemsGlobalAll',
    }),
  },
  watch: {
    dialog() {
      this.reset();
    },
  },
  validations: {
    template_worker: {
      name: {
        required,
      },
      height_frame: {
        required,
        minValue: minValue(1),
      },
      template: {
        required,
      },
      template_assignment: {},
      template_hit: {},
      template_global: {},
    },
  },
  created() {
    this.$v.$touch();

    ServiceTemplates.getAll({
      typeTemplate: 'assignmentAll',
    });

    ServiceTemplates.getAll({
      typeTemplate: 'hitAll',
    });

    ServiceTemplates.getAll({
      typeTemplate: 'globalAll',
    });
  },
  components: { BaseEditor },
};
</script>
