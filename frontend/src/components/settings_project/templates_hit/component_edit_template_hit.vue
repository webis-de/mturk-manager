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
        <span class="headline">Edit HIT Template</span>
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
            v-bind:value="template_hit.name"
            v-bind:error-messages="validation_errors.template_hit.name"
            v-on:input="
              template_hit.name = $event;
              $v.template_hit.name.$touch();
            "
          />
          <v-textarea
            required
            rows="20"
            v-bind:value="template_hit.template"
            label="Template"
            v-bind:error-messages="validation_errors.template_hit.template"
            v-on:input="
              template_hit.template = $event;
              $v.template_hit.template.$touch();
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
import { ServiceTemplates } from '../../../services/templates.service';

export default {
  name: 'ComponentEditTemplateHit',
  mixins: [helpers, validations],
  props: {
    template_hit_current: {},
  },
  data() {
    return {
      template_hit: new Template_HIT(this.template_hit_current),
      dialog: false,
    };
  },
  methods: {
    update(close) {
      if (this.$refs.form.validate()) {
        ServiceTemplates.edit({
          typeTemplate: 'hit',
          templateCurrent: this.template_hit_current,
          templateNew: this.template_hit,
          project: this.project_current,
        }).then(() => {
          ServiceTemplates.cleanup({
            typeTemplate: 'hitAll',
            component: this,
            nameEvent: 'edited',
            template: this.template_hit,
            closeDialog: close === true,
          });
        });
      }
      // console.log(this.project_current);
    },
    reset() {
      (this.template_hit = new Template_HIT(this.template_hit_current)),
      this.$v.$reset();
      this.$v.$touch();
    },
    ...mapActions('moduleProjects', {
      edit_template_hit: 'edit_template_hit',
    }),
  },
  computed: {
    list_templates_hit() {
      return _.orderBy(
        this.project_current.templates_hit,
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
    template_hit: {
      name: {
        required,
      },
      template: {
        required,
        contains_injection_assignments: (value) => value != undefined && value.indexOf(' data-inject_assignments') >= 0,
      },
    },
  },
  created() {
    this.$v.$touch();
  },
  components: {},
};
</script>
