<template>
  <table class="calculation">
    <tbody>
      <tr
        v-for="(calculation, index) in calculations"
        v-bind:key="index"
      >
        <td>{{ calculation.operation }}</td>
        <td class="text-xs-right px-1">
          <base-display-amount
            v-bind:amount="calculation.number"
          >
            <slot></slot>
          </base-display-amount>
        </td>
        <td>
          <v-icon
            v-if="calculation.description"
            class="px-1"
            small
          >arrow_forward</v-icon>
          {{ calculation.description }}
          <base-help v-if="calculation.detail">
            {{ calculation.detail }}
          </base-help>
        </td>
      </tr>
      <tr>
        <td></td>
        <td class="text-xs-right px-1">
          <base-display-amount
            v-bind:amount="result.number"
          >
            <slot></slot>
          </base-display-amount>
        </td>
        <td>
          <v-icon
            v-if="result.description"
            class="px-1"
            small
          >arrow_forward</v-icon>
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
  components: {BaseHelp, BaseDisplayAmount },
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
</style>
