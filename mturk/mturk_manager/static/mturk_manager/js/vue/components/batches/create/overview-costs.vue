<template>
  <v-layout>
    <v-flex>
      <table>
        <tbody>
          <tr>
            <td></td>
            <td
              class="text-xs-right"
            >
              <base-display-amount
                v-bind:amount="costsTotalWithoutFee"
              />
            </td>
            <td>
              <v-icon
                class="px-1"
                small
              >arrow_forward</v-icon>
              <base-display-amount
                v-bind:amount="settingsBatch.reward"
              /> * {{ settingsBatch.count_assignments }} Assignments * {{ object_csv_parsed.data.length }} HITs
            </td>
          </tr>

          <tr>
            <td class="underlinesd">+</td>
            <td
              class="text-xs-right underlined"
            >
              <base-display-amount
                v-bind:amount="fee"
              />
            </td>
            <td>
              <v-icon
                class="px-1"
                small
              >arrow_forward</v-icon>
              MTurk fee</td>
          </tr>

          <tr>
            <td></td>
            <td
              class="text-xs-right underlined-double"
            >
              <base-display-amount
                v-bind:amount="costsTotalWithFee"
              />
            </td>
            <td
            >
              <v-icon
                class="px-1"
                small
              >arrow_forward</v-icon>
              Total
            </td>
          </tr>
        </tbody>
      </table>
    </v-flex>
  </v-layout>
</template>

<script>
import BaseDisplayAmount from '../../base-display-amount';
import {mapGetters} from 'vuex';

export default {
  name: 'OverviewCosts',
  components: { BaseDisplayAmount },
  props: {
    settingsBatch: {
      required: true,
      type: Object,
    },
  },
  computed: {
    costsTotalWithoutFee() {
      if (this.settingsBatch === undefined) return 0;

      console.log(this.object_csv_parsed);
      const reward = parseFloat(this.settingsBatch.reward);
      if (this.object_csv_parsed !== undefined) {
        return (
          reward
          * this.settingsBatch.count_assignments
          * this.object_csv_parsed.data.length
        );
      }
      return reward * this.settingsBatch.count_assignments;
    },
    costsTotalWithFee() {
      let costsWithFee;

      if (this.settingsBatch.count_assignments < 10) {
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
    ...mapGetters('moduleBatches', {
      object_csv_parsed: 'get_object_csv_parsed',
    }),
  },
};
</script>

<style scoped>
  .underlined {
    border-bottom: 1px white solid;
  }
  .underlined-double {
    border-bottom: 3px white double;
  }
</style>
