<template>
  <span>{{ amount_formatted_ }}</span>
</template>

<script>
import helpers from "../mixins/helpers";

export default {
  mixins: [helpers],
  name: "base-display-amount",
  props: {
    amount: {
      required: true,
      type: Number
    }
  },
  computed: {
    amount_formatted_: function() {
      return this.amount_formatted(this.amount);
      return this.amount.toFixed(2) + " $";
    }
  }
};
</script>
