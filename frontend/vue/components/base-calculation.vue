<template>
  <table class="calculation">
    <tbody>
      <tr
        v-for="(calculation, index) in calculations"
        v-bind:key="index"
        v-bind:class="{ 'font-weight-bold': calculation.bold === true }"
      >
        <td>
          <template v-if="calculation.operation === '+'">
            <v-icon>mdi-plus</v-icon>
          </template>
          <template v-else-if="calculation.operation === '-'">
            <v-icon>mdi-minus</v-icon>
          </template>
        </td>
        <td class="text-right px-1">
          <base-display-amount
            v-bind:amount="calculation.number"
          >
            <slot></slot>
          </base-display-amount>
        </td>
        <td class="pl-3">
          {{ calculation.description }}
          <base-help v-if="calculation.detail">
            {{ calculation.detail }}
          </base-help>
        </td>
      </tr>
      <tr
        v-bind:class="{ 'font-weight-bold': result.bold === true }"
      >
        <td></td>
        <td class="text-right px-1">
          <base-display-amount
            v-bind:amount="result.number"
          >
            <slot></slot>
          </base-display-amount>
        </td>
        <td class="pl-3">
          {{ result.description }}
          <base-help v-if="result.detail">
            {{ result.detail }}
          </base-help>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import BaseDisplayAmount from './base-display-amount';
import BaseHelp from './base-help';

export default {
  name: 'BaseCalculation',
  components: { BaseHelp, BaseDisplayAmount },
  props: {
    calculations: {
      required: true,
      type: Array,
    },
    result: {
      required: true,
      type: Object,
    },
  },
};
</script>

<style scoped lang="scss">
  .calculation {
    border-spacing: 0;

    tr {
      height: 30px;
    }

    tr:last-child {
      td {
        border-top: 1px white solid;
        border-bottom: 3px white double;
      }
    }
  }

  .theme--light {
    .calculation {

    tr:last-child {
      td {
        border-top: 1px rgba(0, 0, 0, 0.54) solid;
        border-bottom: 3px rgba(0, 0, 0, 0.54) double;
      }
    }
    }
  }
</style>
