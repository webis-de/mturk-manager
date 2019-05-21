<template>
  <div>
    <h2 class="headline">Default Reject Message</h2>
    <v-layout row>
      <v-flex>
        <!-- v-model="$v.count_assignments_max_per_worker.$model" -->
        <!-- v-on:input="count_assignments_max_per_worker = $event" -->
        <!-- v-model="message_reject" -->
        <v-combobox
          v-bind:value="project_current.message_reject_default"
          v-bind:items="list_messages_reject"
          v-bind:search-input.sync="search"
          label="Enter your default reject message"
          item-text="message"
          item-value="message_lowercase"
          dense
        >
          <template slot="no-data">
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>
                  No results found. Press 'UPDATE' to create a new reject
                  message.
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </template>
        </v-combobox>
      </v-flex>
      <v-flex shrink>
        <v-btn v-bind:disabled="$v.$invalid" color="primary" v-on:click="save"
          >Update</v-btn
        >
      </v-flex>
    </v-layout>

    <v-snackbar
      v-model="snackbar_updated"
      v-bind:timeout="1500"
      bottom
      color="success"
    >
      <v-spacer></v-spacer>
      Updated!
      <v-spacer></v-spacer>
    </v-snackbar>
    <!-- append-icon="clear" -->
    <!-- v-on:input="$emit('update:count_assignments_max_per_worker', try_number($event)); v.settings_batch.count_assignments_max_per_worker.$touch()" -->
    <!-- v-on:click:append="$emit('update:count_assignments_max_per_worker', undefined); v.settings_batch.count_assignments_max_per_worker.$touch()" -->
  </div>
</template>

<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import { required, minValue, maxValue } from 'vuelidate/lib/validators';
import validations from '../../mixins/validations.mixin';
import { Service_Projects } from '../../services/service_projects';
import { ServiceMessages } from '../../services/Service_Messages_Reject';

export default {
  name: 'ComponentMessagesRejectDefault',
  mixins: [validations],
  data() {
    return {
      // message_reject: null,
      search: null,
      snackbar_updated: false,
    };
  },
  methods: {
    save() {
      Service_Projects.set_message_reject_default({
        project: this.project_current,
        message_reject: this.search,
      }).then(() => {
        this.snackbar_updated = true;
      });
    },
  },
  computed: {
    ...mapGetters('moduleMessages', {
      list_messages_reject: 'get_list_messages_reject',
    }),
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  created() {
    // ServiceMessages.loadAll();
  },
  validations: {},
};
</script>

<style scoped></style>
