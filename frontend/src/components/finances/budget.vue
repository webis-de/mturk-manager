<template>
  <div>
    <v-row
      no-gutters
      align="center"
    >
      <v-col>
        <!-- v-model="$v.amount_budget_project.$model" -->
        <!-- v-on:input="amount_budget_project = $event" -->
        <v-row
          align="center"
          no-gutters
        >
          <v-col>
            <v-text-field
              type="number"
              min="1"
              clearable
              v-bind:label="`Maximum Budget for this Project (${amount_formatted(amountBudgetProject, 'unlimited')})`"
              v-bind:error-messages="
                validation_errors.amountBudgetProject
              "
              v-bind:value="amountBudgetProject"
              v-on:input="processInput($event)"
            />
          </v-col>
          <v-col class="shrink">
            <div
              class="text-no-wrap"
            >
              ct, in Dollar: {{ amount_formatted(amountBudgetProject, 'unlimited') }}
            </div>
          </v-col>
        </v-row>
      </v-col>
      <v-col class="pl-3 shrink">
        <v-btn
          v-bind:disabled="$v.$invalid || isActiveAutosave"
          v-bind:loading="isLoading"
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
    <!-- v-on:input="$emit('update:amount_budget_project', try_number($event)); v.settings_batch.amount_budget_project.$touch()" -->
    <!-- v-on:click:append="$emit('update:amount_budget_project', undefined); v.settings_batch.amount_budget_project.$touch()" -->
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { minValue, required, helpers as helpersValidation } from 'vuelidate/lib/validators';
import or from 'vuelidate/src/validators/or';
import _ from 'lodash';
import validations from '../../mixins/validations.mixin';
import { ServiceProjects } from '../../services/projects.service';
import helpers from '../../mixins/helpers.mixin';
// const mustBeCool = (value) => !helpersValidation.req(value) || value > 1;

const validBudget = helpersValidation.withParams(
  { type: 'validBudget' },
  (value) => !helpersValidation.req(value) || value > 0,
);

export default {
  name: 'Budget',
  mixins: [validations, helpers],
  data() {
    return {
      // amountBudgetProject: null,
      snackbar_updated: false,
      isLoading: false,
    };
  },
  computed: {
    isActiveAutosave() {
      return this.$store.state.module_app.isActiveAutosave;
    },
    changed() {},
    amountBudgetProject: {
      get() {
        return this.project_current.amount_budget_max;
      },
      set(value) {
        this.project_current.amount_budget_max = value;
      },
    },
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  // created() {
  //   this.amountBudgetProject = this.project_current.amount_budget_max;
  // },
  methods: {
    processInput(value) {
      this.$v.amountBudgetProject.$touch();
      this.amountBudgetProject = this.tryInteger(value !== null && value.trim() === '' ? null : value);

      if (this.$v.$invalid === false && this.isActiveAutosave === true) {
        this.saveDebounced();
      }
    },
    saveDebounced: _.debounce(function () {
      this.save();
    }, 500),
    save() {
      this.isLoading = true;
      ServiceProjects.setAmountBudgetProject({
        project: this.project_current,
        amountBudgetProject: this.amountBudgetProject,
      }).then(() => {
        this.snackbar_updated = true;
        this.isLoading = false;
      });
    },
    ...mapActions('moduleProjects', {
      set_amount_budget_project:
        'set_amount_budget_project',
    }),
  },
  validations: {
    amountBudgetProject: {
      validBudget,
      // required,
      // mustBeCool,
      // minValue: minValue(1),

      // foo: (value) => {
      //   return false
      // },
    },
  },
};
</script>

<style scoped>

</style>
