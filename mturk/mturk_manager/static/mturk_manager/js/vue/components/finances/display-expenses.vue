<template>
  <v-layout>
    <v-flex>
      <table>
        <tbody>
          <tr>
            <td>
              Costs so far
              <base-help>
                The total costs of the approved assignments
              </base-help>
            </td>
            <td>
              <base-display-amount
                v-if="expenses.sum_costs_so_far !== undefined"

                v-bind:amount="expenses.sum_costs_so_far"
              />
              <v-progress-circular
                v-else
                indeterminate
                size="20"
                width="2"
              ></v-progress-circular>
            </td>
          </tr>

          <tr>
            <td>
              Pending costs
              <base-help>
                The remaining costs you would pay if all remaining assignments would be approved
              </base-help>
            </td>
            <td>
              <base-display-amount
                v-if="expenses.sum_costs_pending !== undefined"

                v-bind:amount="expenses.sum_costs_pending"
              />
              <v-progress-circular
                v-else
                indeterminate
                size="20"
                width="2"
              ></v-progress-circular>
            </td>
          </tr>

          <tr>
            <td>
              Max costs
              <base-help>
                The total costs of all batches
              </base-help>
            </td>
            <td>
              <base-display-amount
                v-if="costsTotal !== undefined"

                v-bind:amount="costsTotal"
              />
              <v-progress-circular
                v-else
                indeterminate
                size="20"
                width="2"
              ></v-progress-circular>
            </td>
          </tr>
        </tbody>
      </table>
    </v-flex>
  </v-layout>
</template>

<script>
import {
  mapState,
} from 'vuex';
import BaseDisplayAmount from '../base-display-amount';
import BaseHelp from '../base-help';

export default {
  name: 'DisplayExpenses',
  components: {
    BaseHelp,
    BaseDisplayAmount,
  },
  props: {
    expenses: {
      required: true,
      type: Object,
    },
  },
  computed: {
    costsTotal() {
      const costsTotal = this.expenses.sum_costs_so_far + this.expenses.sum_costs_pending;

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
