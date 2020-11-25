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
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';
import BaseCalculation from '../../base-calculation';
import helpers from '../../../mixins/helpers.mixin';

export default {
  name: 'OverviewCosts',
  components: { BaseCalculation },
  mixins: [helpers],
  props: {
    settingsBatch: {
      required: true,
      type: SettingsBatch,
    },
  },
  computed: {
    countAssignments() {
      return this.settingsBatch.count_assignments === undefined ? this.settingsBatch.countAssignments : this.settingsBatch.count_assignments;
    },
    result() {
      return {
        number: this.costsTotalWithFee,
        description: 'Total',
        bold: true,
      };
    },
    calculations() {
      console.warn(this.settingsBatch, 'this.settingsBatch');
      return [
        {
          number: this.costsTotalWithoutFee,
          description: `${this.amount_formatted(this.settingsBatch.reward)}
          * ${this.countAssignments} Assignments
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
      if (this.settingsBatch === null) return 0;

      let reward = parseFloat(this.settingsBatch.reward);
      if (Number.isNaN(reward)) {
        reward = 0;
      }

      let { countAssignments } = this;

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

      return reward * this.countAssignments;
    },
    costsTotalWithFee() {
      let costsWithFee;

      if (this.countAssignments < 10) {
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
