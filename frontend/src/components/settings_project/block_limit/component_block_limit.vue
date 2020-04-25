<template>
  <div>
    <v-row
      align="center"
      no-gutters
    >
      <v-col>
        <!-- v-model="$v.count_assignments_max_per_worker.$model" -->
        <!-- v-on:input="count_assignments_max_per_worker = $event" -->
        <v-text-field
          type="number"
          v-bind:value="project_current.count_assignments_max_per_worker"
          label="Number of Maximal Assignments Per Worker"
          min="1"
          clearable
          v-bind:error-messages="
            validation_errors.count_assignments_max_per_worker
          "
          v-on:input="
            count_assignments_max_per_worker = $event;
            $v.count_assignments_max_per_worker.$touch();
          "
        />
      </v-col>
      <v-col class="pl-3 shrink">
        <v-btn
          v-bind:disabled="$v.$invalid"
          color="primary"
          v-on:click="save"
        >
          Update
        </v-btn>
      </v-col>
    </v-row>

    <v-snackbar
      v-model="snackbar_updated"
      v-bind:timeout="1500"
      bottom
      color="success"
    >
      <v-spacer />
      Updated!
      <v-spacer />
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
import validations from '../../../mixins/validations.mixin';
import { ServiceProjects } from '../../../services/projects.service';

export default {
  name: 'ComponentBlockLimit',
  mixins: [validations],
  data() {
    return {
      count_assignments_max_per_worker: null,
      snackbar_updated: false,
    };
  },
  methods: {
    save() {
      ServiceProjects.setCountAssignmentsMaxPerWorker({
        project: this.project_current,
        countAssignmentsMaxPerWorker: this.count_assignments_max_per_worker,
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
