<template>
  <span>{{ amount_formatted_ }}</span>
</template>

<script>
import helpers from '../mixins/helpers';

export default {
  name: 'BaseDisplayAmount',
  mixins: [helpers],
  props: {
    amount: {
      required: true,
      type: Number,
    },
  },
  computed: {
    amount_formatted_() {
      return this.amount_formatted(this.amount);
    },
  },
};
</script>
