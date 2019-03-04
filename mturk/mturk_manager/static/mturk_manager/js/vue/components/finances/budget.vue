<template>
  <div>
    <h2 class="headline">
      Budget
    </h2>
    <v-layout row>
      <v-flex>
        <!-- v-model="$v.amount_budget_project.$model" -->
        <!-- v-on:input="amount_budget_project = $event" -->
        <v-layout align-center>
          <v-flex>
            <v-text-field
              type="number"
              min="1"
              clearable
              v-bind:label="`Maximum Budget for this Project (${amount_formatted(amountBudgetProject)})`"
              v-bind:error-messages="
                validation_errors.amountBudgetProject
              "
              v-bind:value="project_current.amount_budget_max"
              v-on:input="
                amountBudgetProject = $event;
                $v.amountBudgetProject.$touch();
              "
            ></v-text-field>
          </v-flex>
          <v-flex shrink>
            <div slot="append" class="text-no-wrap">
              ct, in Dollar: {{ amount_formatted(amountBudgetProject) }}
            </div>
          </v-flex>
        </v-layout>
      </v-flex>
      <v-flex shrink>
        <v-btn
          v-bind:disabled="$v.$invalid"
          color="primary"
          v-on:click="save"
        >
          Update
        </v-btn>
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
    <!-- v-on:input="$emit('update:amount_budget_project', try_number($event)); v.settings_batch.amount_budget_project.$touch()" -->
    <!-- v-on:click:append="$emit('update:amount_budget_project', undefined); v.settings_batch.amount_budget_project.$touch()" -->
  </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex';
import { minValue } from 'vuelidate/lib/validators';
import validations from '../../mixins/validations';
import {Service_Projects} from '../../services/service_projects';
import helpers from '../../mixins/helpers';

export default {
  name: 'Budget',
  mixins: [validations, helpers],
  data() {
    return {
      amountBudgetProject: null,
      snackbar_updated: false,
    };
  },
  computed: {
    changed() {},
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  methods: {
    save() {
      Service_Projects.setAmountBudgetProject({
        project: this.project_current,
        amountBudgetProject: this.amountBudgetProject,
      }).then(() => {
        this.snackbar_updated = true;
      });
    },
    ...mapActions('moduleProjects', {
      set_amount_budget_project:
        'set_amount_budget_project',
    }),
  },
  validations: {
    amountBudgetProject: {
      minValue: minValue(1),
    },
  },
};
</script>

<style scoped>

</style>