<template>
  <div class="subheading">
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
      return {
        number: parseInt(this.get_balance(), 10) * 100 - this.expenses.sum_costs_submitted,
        description: 'Projected Balance',
      };
    },
    calculations() {
      return [
        {
          number: parseInt(this.get_balance(), 10) * 100,
          description: 'Current Balance',
          bold: true,
        },
        {
          operation: '-',
          number: this.expenses.sum_costs_submitted,
          description: 'Submitted Assignments',
        },
      ];
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
