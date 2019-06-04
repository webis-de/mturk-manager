<template>
  <div class="subheading">
    {{expenses}}
    <!--Current balance:-->
    <base-calculation
      v-if="get_balance() !== null"
      v-bind:calculations="calculations"
      v-bind:result="result"
    >
      <v-progress-circular
        indeterminate
        size="20"
        width="2"
      />
    </base-calculation>
    <v-progress-circular
      v-else
      indeterminate
      size="20"
      width="2"
    />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import BaseCalculation from '../base-calculation';

export default {
  name: 'ComponentShowBalance',
  components: {
    BaseCalculation,
  },
  props: {
    expenses: {
      required: true,
      type: Object,
    },
  },
  data() {
    return {
      updating: false,
    };
  },
  computed: {
    result() {
      let result = this.get_balance()
      - this.expenses.sum_costs_submitted;

      if (!Number.isNaN(result) && this.expenses.sum_costs_pending !== undefined) {
        result -= this.expenses.sum_costs_pending;
      }

      if (Number.isNaN(result)) {
        result = undefined;
      }

      return {
        number: result,
        description: 'Projected Balance',
      };
    },
    calculations() {
      const result = [
        {
          number: this.get_balance(),
          description: 'Current Balance',
          bold: true,
        },
        {
          operation: '-',
          number: this.expenses.sum_costs_submitted,
          description: 'Submitted Assignments',
        },
      ];

      if (this.expenses.sum_costs_submitted !== undefined && this.expenses.sum_costs_pending !== undefined) {
        result.push({
          operation: '-',
          number: this.expenses.sum_costs_pending,
          description: 'Open Assignments',
        });
      }

      return result;
    },
    show_spinner() {
      return this.updating || this.get_balance === undefined;
    },
    ...mapGetters('module_finances', {
      get_balance: 'get_balance',
    }),
  },
};
</script>

<style lang="scss" scoped></style>
