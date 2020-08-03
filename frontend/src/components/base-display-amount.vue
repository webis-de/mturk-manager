<template>
  <span class="roboto-mono">
    <template v-if="amount !== undefined">
      {{ amount_formatted_ }}
    </template>
    <slot v-else></slot>
  </span>
</template>

<script>
import helpers from '../mixins/helpers.mixin';

export default {
  name: 'BaseDisplayAmount',
  mixins: [helpers],
  props: {
    amount: {
      required: false,
      type: Number,
      default: undefined,
    },
    currency: {
      required: false,
      type: String,
      default: undefined,
    },
  },
  computed: {
    amount_formatted_() {
      return this.amount_formatted(Math.round(this.amount), null, this.currency);
    },
  },
};
</script>
