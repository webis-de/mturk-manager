<template>
  <v-layout>
    <v-flex>
      <v-card>
        <v-card-title>
          {{title}} Costs ($)
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
            />
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
    title() {
      if (this.typeItem === 'batches') {
        return 'Batch';
      } else if (this.typeItem === 'hits') {
        return 'HIT';
      } else if (this.typeItem === 'assignments') {
        return 'Assignment';
      }
    },
    calculations() {
      const result = [
        {
          operation: '',
          number: this.expenses.sum_costs_approved,
          description: 'Approved',
          detail: 'The costs already paid',
        },
        {
          operation: '+',
          number: this.expenses.sum_costs_rejected,
          description: 'Rejected',
          detail: 'The costs you would have paid approving the rejected assignments',
        },
      ];

      if (this.typeItem !== 'assignments') {
        result.push({
          operation: '+',
          number: this.expenses.sum_costs_dead,
          description: 'Expired',
          detail: 'The costs you would have paid if all expired assignments would\'ve been approved',
        });
      }

      result.push({
        operation: '+',
        number: this.expenses.sum_costs_submitted,
        description: 'Submitted',
        detail: 'The costs you would pay if all currently submitted assignments would be approved',
      });

      if (this.typeItem !== 'assignments') {
        result.push({
          operation: '+',
          number: this.expenses.sum_costs_pending,
          description: 'Open',
          detail: 'The costs you would pay if all open assignments would be processed by workers and approved by you',
        });
      }

      return result;
    },
    costsTotal() {
      let costsTotal = this.expenses.sum_costs_approved
                       + this.expenses.sum_costs_rejected
                       + this.expenses.sum_costs_submitted;

      if (this.typeItem !== 'assignments') {
        costsTotal += this.expenses.sum_costs_pending
                       + this.expenses.sum_costs_dead;
      }

      if (Number.isNaN(costsTotal) === true) {
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
