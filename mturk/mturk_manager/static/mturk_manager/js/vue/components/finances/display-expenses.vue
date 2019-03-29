<template>
  <v-layout>
    <v-flex>
      <v-card>
        <v-card-title>
          Costs
        </v-card-title>

        <v-card-text>
          <base-calculation
            v-bind:calculations="calculations"
            v-bind:result="{
              number: costsTotal,
              description: 'Total',
            }"
          >
            <v-progress-circular
              indeterminate
              size="20"
              width="2"
            ></v-progress-circular>
          </base-calculation>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import {
  mapState,
} from 'vuex';
import BaseCalculation from '../base-calculation';

export default {
  name: 'DisplayExpenses',
  components: {
    BaseCalculation,
  },
  props: {
    expenses: {
      required: true,
      type: Object,
    },
    typeItem: {
      required: true,
      type: String,
    },
  },
  computed: {
    calculations()  {
      const result = [
        {
          operation: '',
          number: this.expenses.sum_costs_so_far,
          description: 'So far',
          detail: 'The costs already paid',
        },
      ];

      result.push({
        operation: '+',
        number: this.expenses.sum_costs_submitted,
        description: 'Submitted',
        detail: 'The costs if all currently submitted assignments would be approved',
      });

      if(this.typeItem !== 'assignments') {
        result.push({
          operation: '+',
          number: this.expenses.sum_costs_pending,
          description: 'Pending',
          detail: 'The costs of the remaining assignments',
        });
      }

      return result;
    },
    costsTotal() {
      let costsTotal = this.expenses.sum_costs_so_far + this.expenses.sum_costs_submitted;

      if(this.typeItem !== 'assignments') {
         costsTotal += this.expenses.sum_costs_pending
      }

      if(Number.isNaN(costsTotal) === true) {
        return undefined;
      }

      return costsTotal;
    },
    ...mapState('module_app', ['use_sandbox']),
  },
};
</script>

<style scoped>
  tr {
    height: 30px;
  }

  td:nth-child(2) {
    text-align: right;
    padding-left: 20px;
  }
</style>
