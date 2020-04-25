<template>
  <v-dialog
    v-model="dialog"
    max-width="80%"
    persistent
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
        <span class="headline">Edit Global Template</span>
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
            v-bind:value="template_global.name"
            v-bind:error-messages="validation_errors.template_global.name"
            v-on:input="
              template_global.name = $event;
              $v.template_global.name.$touch();
            "
          />
          <v-textarea
            required
            rows="20"
            v-bind:value="template_global.template"
            label="Template"
            v-bind:error-messages="validation_errors.template_global.template"
            v-on:input="
              template_global.template = $event;
              $v.template_global.template.$touch();
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
import Template_Global from '../../../classes/template_global';
import { ServiceTemplates } from '../../../services/service_templates';

export default {
  name: 'ComponentEditTemplateGlobal',
  mixins: [helpers, validations],
  props: {
    template_global_current: {},
  },
  data() {
    return {
      template_global: new Template_Global(this.template_global_current),
      dialog: false,
    };
  },
  methods: {
    update(close) {
      if (this.$refs.form.validate()) {
        ServiceTemplates.edit({
          typeTemplate: 'global',
          templateCurrent: this.template_global_current,
          templateNew: this.template_global,
          project: this.project_current,
        }).then(() => {
          ServiceTemplates.cleanup({
            typeTemplate: 'globalAll',
            component: this,
            nameEvent: 'edited',
            template: this.template_global,
            closeDialog: close === true,
          });
        });
      }
      // console.log(this.project_current);
    },
    reset() {
      (this.template_global = new Template_Global(
        this.template_global_current,
      )),
      this.$v.$reset();
      this.$v.$touch();
    },
    ...mapActions('moduleProjects', {
      edit_template_global: 'edit_template_global',
    }),
  },
  computed: {
    list_templates_global() {
      return _.orderBy(
        this.project_current.templates_global,
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
    template_global: {
      name: {
        required,
      },
      template: {
        required,
      },
    },
  },
  created() {
    this.$v.$touch();
  },
  components: {},
};
</script>
