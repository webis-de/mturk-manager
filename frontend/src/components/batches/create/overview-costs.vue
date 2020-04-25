<template>
  <v-layout>
    <v-flex>
      <base-calculation
        v-bind:calculations="calculations"
        v-bind:result="result"
      />
    </v-flex>
  </v-layout>
</template>

<script>
import BaseCalculation from '../../base-calculation';
import helpers from '../../../mixins/helpers.mixin';

export default {
  name: 'OverviewCosts',
  components: { BaseCalculation },
  mixins: [helpers],
  props: {
  },
  computed: {
    result() {
      return {
        number: this.costsTotalWithFee,
        description: 'Total',
        bold: true,
      };
    },
    calculations() {
      return [
        {
          number: this.costsTotalWithoutFee,
          description: `${this.amount_formatted(this.$store.state.moduleBatches.objectSettingsBatch.reward)}
          * ${this.$store.state.moduleBatches.objectSettingsBatch.count_assignments} Assignments
          * ${this.csv.data.length} HITs`,
        },
        {
          operation: '+',
          number: this.fee,
          description: 'MTurk fee',
        },
      ];
    },
    csv() {
      return this.$store.state.moduleBatches.objectCSVParsed;
    },
    costsTotalWithoutFee() {
      if (this.$store.state.moduleBatches.objectSettingsBatch === null) return 0;

      let reward = parseFloat(this.$store.state.moduleBatches.objectSettingsBatch.reward);
      if (Number.isNaN(reward)) {
        reward = 0;
      }

      let countAssignments = this.$store.state.moduleBatches.objectSettingsBatch.count_assignments;

      if (countAssignments === undefined) {
        countAssignments = 0;
      }

      if (this.csv !== undefined) {
        return (
          reward
          * countAssignments
          * this.csv.data.length
        );
      }

      return reward * this.$store.state.moduleBatches.objectSettingsBatch.count_assignments;
    },
    costsTotalWithFee() {
      let costsWithFee;

      if (this.$store.state.moduleBatches.objectSettingsBatch.count_assignments < 10) {
        costsWithFee = this.costsTotalWithoutFee * 1.2;
      } else {
        costsWithFee = this.costsTotalWithoutFee * 1.4;
      }

      this.$emit('updated_costs_with_fee', costsWithFee);

      return costsWithFee;
    },
    fee() {
      return this.costsTotalWithFee - this.costsTotalWithoutFee;
    },
  },
};
</script>

<style scoped>
</style>
