<template>
  <div>
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
          <span class="headline">Add Global Template</span>
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
  </div>
</template>

<script>
// import ComponentFormSettingsBatch from './component_form_settings_batch';
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';

import { required, minValue } from 'vuelidate/lib/validators';
import validations from '../../../mixins/validations.mixin';
import { ServiceTemplates } from '../../../services/service_templates';

export default {
  name: 'ComponentAddTemplateGlobal',
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
        ServiceTemplates.create({
          typeTemplate: 'global',
          template: {
            name: this.name,
            template: this.template,
          },
          project: this.project_current,
        }).then((template) => {
          ServiceTemplates.cleanup({
            typeTemplate: 'globalAll',
            component: this,
            nameEvent: 'created',
            template,
          });
        });
      }
    },
    ...mapActions('moduleProjects', {
      create_template_global: 'create_template_global',
    }),
  },
  computed: {
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  components: {},
};
</script>
