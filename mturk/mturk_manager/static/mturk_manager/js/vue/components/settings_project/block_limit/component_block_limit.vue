<template>
  <div>
    <h2 class="headline">Limit Block</h2>
    <v-layout row>
      <v-flex>
        <!-- v-model="$v.count_assignments_max_per_worker.$model" -->
        <!-- v-on:input="count_assignments_max_per_worker = $event" -->
        <v-text-field
          type="number"
          v-bind:value="project_current.count_assignments_max_per_worker"
          v-on:input="
            count_assignments_max_per_worker = $event;
            $v.count_assignments_max_per_worker.$touch();
          "
          label="Number of Maximal Assignments Per Worker"
          min="1"
          clearable
          v-bind:error-messages="
            validation_errors.count_assignments_max_per_worker
          "
        ></v-text-field>
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
import validations from '../../../mixins/validations';
import { Service_Projects } from '../../../services/service_projects';

export default {
  name: 'component-block-limit',
  mixins: [validations],
  data() {
    return {
      count_assignments_max_per_worker: null,
      snackbar_updated: false,
    };
  },
  methods: {
    save() {
      Service_Projects.set_count_assignments_max_per_worker({
        project: this.project_current,
        count_assignments_max_per_worker: this.count_assignments_max_per_worker,
      }).then(() => {
        this.snackbar_updated = true;
      });
    },
    ...mapActions('moduleProjects', {
      set_count_assignments_max_per_worker:
        'set_count_assignments_max_per_worker',
    }),
  },
  computed: {
    changed() {},
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  components: {},
  validations: {
    count_assignments_max_per_worker: {
      minValue: minValue(1),
    },
  },
};
</script>

<style scoped></style>
