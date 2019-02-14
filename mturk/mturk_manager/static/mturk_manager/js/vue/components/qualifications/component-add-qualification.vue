<template>
  <v-dialog v-model="show_dialog" max-width="800px" persistent>
    <v-btn
      slot="activator"
      v-on:click="policy_to_be_edited = null"
      color="primary"
      dark
      class="mb-2"
      >New Qualification</v-btn
    >
    <v-card>
      <v-card-title>
        <span class="headline">{{ title_dialog }}</span>
      </v-card-title>
      {{ is_form_valid }}
      <v-card-text>
        <v-container grid-list-md>
          <v-form v-model="is_form_valid">
            <v-layout row align-center wrap>
              <v-flex xs12 md10>
                <v-text-field
                  v-model="object_qualification.name_database"
                  label="Name"
                  hint="Will not be shown to the workers!"
                  persistent-hint
                ></v-text-field>
              </v-flex>
              <!--  <v-flex xs12 md2>
                                        <v-switch v-bind:label="object_qualification.is_active ? 'Active' : 'Inactive'" v-model="object_qualification.is_active"></v-switch>
                                    </v-flex> -->
            </v-layout>
            <v-layout wrap align-center>
              <v-flex xs12>
                <v-text-field
                  v-model="object_qualification.description_database"
                  label="Description"
                  hint="Will not be shown to the workers!"
                  persistent-hint
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-layout wrap align-center>
              <v-flex xs12>
                <v-text-field
                  v-model="object_qualification.keywords"
                  label="Keywords"
                  hint="Separated by a comma."
                  persistent-hint
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-layout wrap>
              <v-flex xs12>
                <v-checkbox
                  label="Custom name and description for MTurk?"
                  v-model="add_custom_mturk"
                ></v-checkbox>
              </v-flex>
            </v-layout>
            <template v-if="add_custom_mturk">
              <v-layout row align-center wrap>
                <v-flex xs12>
                  <v-text-field
                    v-model="object_qualification.name_mturk"
                    label="Name displayed in MTurk"
                    hint="Will be a random token by default."
                    persistent-hint
                  ></v-text-field>
                </v-flex>
              </v-layout>
              <v-layout wrap align-center>
                <v-flex xs12>
                  <v-text-field
                    v-model="object_qualification.description_mturk"
                    label="Description displayed in MTurk"
                    hint="Will be a random token by default."
                    persistent-hint
                  ></v-text-field>
                </v-flex>
              </v-layout>
            </template>
          </v-form>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="blue darken-1"
          flat
          v-bind:disabled="is_creating"
          v-on:click.native="clear"
          >Cancel</v-btn
        >
        <v-btn
          color="blue darken-1"
          v-bind:loading="is_creating"
          flat
          v-on:click.native="save"
          >Save</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
// import { Policy } from '../../store/modules/policies.js';
import { Qualification } from "../../classes/qualifications.js";

// import ComponentShowBalance from './component-show-balance.vue';
// import ComponentShowMoneySpent from './component-show-money-spent.vue';
// import ComponentShowBatches from './component-show-batches.vue';
export default {
  name: "component-add-qualification",
  props: {},
  data() {
    return {
      show_dialog: false,
      is_creating: false,
      is_form_valid: false,
      add_custom_mturk: false,
      title_dialog: "Add Qualification",

      object_qualification: new Qualification()
    };
  },
  computed: {},
  methods: {
    save: function() {
      this.is_creating = true;
      this.add_qualification(this.object_qualification).then(() => {
        this.clear();
      });
    },
    clear: function() {
      this.show_dialog = false;
      this.is_creating = false;
      this.object_qualification = new Qualification();
    },
    ...mapActions("moduleQualifications", {
      add_qualification: "add_qualification"
    })
  },
  watch: {}
};
</script>
