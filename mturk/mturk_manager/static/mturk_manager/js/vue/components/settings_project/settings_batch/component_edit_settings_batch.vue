<template>
  <v-dialog v-model="dialog" max-width="80%">
    <v-btn slot="activator" icon small>
      <v-icon color="warning">edit</v-icon>
    </v-btn>
    <v-card>
      <v-card-title>
        <span class="headline">Edit Batch Profile</span>
        <v-spacer></v-spacer>
        <v-btn icon v-on:click="dialog = false">
          <v-icon>close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-form ref="form" lazy-validation>
          <v-text-field
            required
            v-bind:value="settings_batch.name"
            label="Name"
            v-on:input="
              settings_batch.name = $event;
              $v.settings_batch.name.$touch();
            "
            v-bind:error-messages="validation_errors.settings_batch.name"
          ></v-text-field>

          <component-form-settings-batch
            v-bind.sync="settings_batch"
            v-bind:v="$v"
            v-bind:validation_errors="validation_errors"
          ></component-form-settings-batch>
        </v-form>

        <v-btn
          class="ml-0"
          color="primary"
          v-on:click="update()"
          v-bind:disabled="$v.$invalid"
          >Update</v-btn
        >
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
	        flat
	        v-on:click="show_snackbar = false"
	    >
	        Close
	    </v-btn>
	</v-snackbar> -->
</template>
<script>
import { mapState, mapMutations, mapActions, mapGetters } from "vuex";
import _ from "lodash";
import { required, minValue, maxValue } from "vuelidate/lib/validators";
import ComponentFormSettingsBatch from "./component_form_settings_batch";
import settings_batch from "../../../mixins/settings_batch";
import validations from "../../../mixins/validations";
import { Service_Settings_Batch } from "../../../services/service_settings_batch";

export default {
  name: "component-edit-settings-batch",
  mixins: [validations, settings_batch],
  props: {
    settings_batch_current: {}
  },
  data() {
    return {
      dialog: false,
      disable_unique_name: true,
      name_not_unique: true
    };
  },
  methods: {
    update() {
      if (this.$refs.form.validate()) {
        Service_Settings_Batch.edit({
          settings_batch_current: this.settings_batch_current,
          settings_batch_new: this.settings_batch,
          project: this.project_current
        });

        this.dialog = false;
        this.$emit("edited");
        this.reset();
      }
    },
    reset() {
      this.update_fields();
      this.$v.$reset();
      this.$v.$touch();
    },
    ...mapActions("moduleProjects", {
      edit_settings_batch: "edit_settings_batch"
    })
  },
  watch: {
    dialog() {
      this.reset();
    }
  },
  created() {
    this.$v.$touch();
  },
  components: {
    ComponentFormSettingsBatch
  }
};
</script>
