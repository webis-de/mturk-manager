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
              >
                arrow_forward
              </v-icon>
              <base-display-amount
                v-bind:amount="$store.state.moduleBatches.objectSettingsBatch.reward"
              /> * {{ $store.state.moduleBatches.objectSettingsBatch.count_assignments }}
              Assignments * {{ csv.data.length }} HITs
            </td>
          </tr>

          <tr>
            <td class="underlinesd">
              +
            </td>
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
              >
                arrow_forward
              </v-icon>
              MTurk fee
            </td>
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
            <td>
              <v-icon
                class="px-1"
                small
              >
                arrow_forward
              </v-icon>
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

export default {
  name: 'OverviewCosts',
  components: { BaseDisplayAmount },
  props: {
  },
  computed: {
    csv() {
      return this.$store.state.moduleBatches.objectCSVParsed;
    },
    costsTotalWithoutFee() {
      if (this.$store.state.moduleBatches.objectSettingsBatch === null) return 0;

      console.log(this.csv);
      const reward = parseFloat(this.$store.state.moduleBatches.objectSettingsBatch.reward);
      if (this.csv !== undefined) {
        return (
          reward
          * this.$store.state.moduleBatches.objectSettingsBatch.count_assignments
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
  .underlined {
    border-bottom: 1px white solid;
  }
  .underlined-double {
    border-bottom: 3px white double;
  }
</style>
