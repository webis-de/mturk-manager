<template>
  <div>
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

            <template-worker-sandbox
              v-bind:value="template_worker.template"
              label="Template"
              v-on:input="
                template_worker.template = $event;
                $v.template_worker.template.$touch();
              "
            />
            <!--              v-bind:error-messages="validation_errors.template_worker.template"-->

            <v-select
              v-bind:value="template_worker.template_assignment"
              v-bind:items="arrayTemplatesAssignment"
              label="Assignment Template"
              item-text="name"
              item-value="id"
              v-bind:error-messages="
                validation_errors.template_worker.template_assignment
              "
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
              v-on:input="
                template_worker.template_global = $event;
                $v.template_worker.template_global.$touch();
              "
            />
            <!-- <v-text-field
			            required
			  			v-bind:value="template"
			            v-on:input="template=$event; $v.template.$touch()"
			            label="Template"
		        		v-bind:error-messages="validation_errors.template"
			        ></v-text-field> -->

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
  </div>
</template>

<script>
import {
  mapState, mapGetters,
} from 'vuex';
import _ from 'lodash';

import { required, minValue } from 'vuelidate/lib/validators';
import validations from '../../../mixins/validations.mixin';
import helpers from '../../../mixins/helpers.mixin';
import { TemplateWorker } from '../../../classes/template_worker';
import { ServiceTemplates } from '../../../services/templates.service';
import BaseEditor from '../../../modules/app/components/base-editor';
import TemplateWorkerSandbox from '../../../modules/template/components/template-worker-sandbox';

export default {
  name: 'ComponentAddTemplateWorker',
  components: { TemplateWorkerSandbox, BaseEditor },
  mixins: [helpers, validations],
  data() {
    return {
      template_worker: new TemplateWorker(),
      dialog: false,
    };
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
  methods: {
    reset() {
      this.template_worker = new TemplateWorker();
      this.$v.$reset();
    },
    create() {
      if (this.$refs.form.validate()) {
        ServiceTemplates.create({
          typeTemplate: 'worker',
          template: this.template_worker,
          project: this.project_current,
        }).then((template) => {
          ServiceTemplates.cleanup({
            typeTemplate: 'workerAll',
            component: this,
            nameEvent: 'created',
            template,
          });

          // ServiceTemplates.getAll({
          //   typeTemplate: 'workerAll',
          //   force: true,
          // });
        });
      }
    },
  },
};
</script>
