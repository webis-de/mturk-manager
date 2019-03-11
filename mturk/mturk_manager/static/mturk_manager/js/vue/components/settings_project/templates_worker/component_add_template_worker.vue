<template>
  <div>
    <v-dialog v-model="dialog">
      <v-btn slot="activator" color="primary" small
        ><v-icon>add</v-icon> Add Template</v-btn
      >
      <v-card>
        <v-card-title>
          <span class="headline">Add Worker Template</span>
          <v-spacer></v-spacer>
          <v-btn icon v-on:click="dialog = false">
            <v-icon>close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              required
              label="Name"
              v-bind:value="template_worker.name"
              v-on:input="
                template_worker.name = $event;
                $v.template_worker.name.$touch();
              "
              v-bind:error-messages="validation_errors.template_worker.name"
            ></v-text-field>
            <v-text-field
              type="number"
              required
              v-bind:value="template_worker.height_frame"
              v-on:input="
                template_worker.height_frame = try_number($event);
                $v.template_worker.height_frame.$touch();
              "
              label="Height"
              v-bind:error-messages="
                validation_errors.template_worker.height_frame
              "
            ></v-text-field>

            <v-textarea
              required
              rows="20"
              v-bind:value="template_worker.template"
              v-on:input="
                template_worker.template = $event;
                $v.template_worker.template.$touch();
              "
              label="Template"
              v-bind:error-messages="validation_errors.template_worker.template"
            ></v-textarea>

            <v-select
              v-bind:value="template_worker.template_assignment"
              v-on:input="
                template_worker.template_assignment = $event;
                $v.template_worker.template_assignment.$touch();
              "
              v-bind:items="arrayTemplatesAssignment"
              label="Assignment Template"
              item-text="name"
              item-value="id"
              v-bind:error-messages="
                validation_errors.template_worker.template_assignment
              "
            ></v-select>

            <v-select
              v-bind:value="template_worker.template_hit"
              v-on:input="
                template_worker.template_hit = $event;
                $v.template_worker.template_hit.$touch();
              "
              v-bind:items="arrayTemplatesHIT"
              label="HIT Template"
              item-text="name"
              item-value="id"
              v-bind:error-messages="
                validation_errors.template_worker.template_hit
              "
            ></v-select>

            <v-select
              v-bind:value="template_worker.template_global"
              v-on:input="
                template_worker.template_global = $event;
                $v.template_worker.template_global.$touch();
              "
              v-bind:items="arrayTemplatesGlobal"
              label="Global Template"
              item-text="name"
              item-value="id"
              v-bind:error-messages="
                validation_errors.template_worker.template_global
              "
            ></v-select>
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
            v-on:click="create()"
            v-bind:disabled="$v.$invalid"
            >Create</v-btn
          >
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
// import ComponentFormSettingsBatch from './component_form_settings_batch';
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';

import { required, minValue } from 'vuelidate/lib/validators';
import validations from '../../../mixins/validations';
import helpers from '../../../mixins/helpers';
import Template_Worker from '../../../classes/template_worker';
import { Service_Templates } from '../../../services/service_templates';

export default {
  name: 'ComponentAddTemplateWorker',
  mixins: [helpers, validations],
  data() {
    return {
      template_worker: new Template_Worker(),
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
        template => template.name,
      );
    },
    arrayTemplatesHIT() {
      if (this.arrayTemplatesHITAll === null) {
        return [];
      }

      return _.orderBy(
        this.arrayTemplatesHITAll,
        template => template.name,
      );
    },
    arrayTemplatesGlobal() {
      if (this.arrayTemplatesGlobalAll === null) {
        return [];
      }

      return _.orderBy(
        this.arrayTemplatesGlobalAll,
        template => template.name,
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
    Service_Templates.getAll({
      typeTemplate: 'assignmentAll',
    });

    Service_Templates.getAll({
      typeTemplate: 'hitAll',
    });

    Service_Templates.getAll({
      typeTemplate: 'globalAll',
    });
  },
  methods: {
    reset() {
      this.template_worker = new Template_Worker();
      this.$v.$reset();
    },
    create() {
      if (this.$refs.form.validate()) {
        Service_Templates.create({
          typeTemplate: 'worker',
          template: this.template_worker,
          project: this.project_current,
        }).then((template) => {
          Service_Templates.cleanup({
            typeTemplate: 'workerAll',
            component: this,
            nameEvent: 'created',
            template,
          });

          // Service_Templates.getAll({
          //   typeTemplate: 'workerAll',
          //   force: true,
          // });
        });
      }
    },
  },
};
</script>
