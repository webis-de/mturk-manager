<template>
  <div>
    <v-dialog v-model="dialog" max-width="80%">
      <v-btn
        slot="activator"
        color="primary"
        small
        v-bind:disabled="is_disabled"
        ><v-icon>add</v-icon> Add Profile</v-btn
      >
      <v-card>
        <v-card-title>
          <span class="headline">Add Batch Profile</span>
          <v-spacer></v-spacer>
          <v-btn icon v-on:click="dialog = false">
            <v-icon>close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
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
import { mapState, mapMutations, mapActions, mapGetters } from "vuex";
import _ from "lodash";
import ComponentFormSettingsBatch from "./component_form_settings_batch";
import settings_batch from "../../../mixins/settings_batch";
import validations from "../../../mixins/validations";
import { Service_Settings_Batch } from "../../../services/service_settings_batch";

export default {
  name: "component-add-settings-batch",
  mixins: [validations, settings_batch],
  data() {
    return {
      dialog: false
    };
  },
  methods: {
    create() {
      if (this.$refs.form.validate()) {
        Service_Settings_Batch.create({
          settings_batch: this.settings_batch,
          project: this.project_current
        }).then(() => {
          this.dialog = false;
          this.$emit("created");
          this.reset();
        });
      }
    },
    reset() {
      this.update_fields();
      this.$v.$reset();
    }
  },
  computed: {
    is_disabled() {
      return _.size(_.get(this.project_current, "templates_worker", [])) == 0;
    }
  },
  watch: {
    dialog() {
      this.reset();
    }
  },
  components: {
    ComponentFormSettingsBatch
  }
};
</script>
