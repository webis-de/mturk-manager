<template>
  <v-layout>
    <v-flex shrink>
      <v-layout>
        <v-flex>
          <br>
          +
        </v-flex>
      </v-layout>
    </v-flex>
    <v-flex shrink>
      <v-layout>
        <v-flex />
        <v-flex
          class="text-xs-right"
        >
          <base-display-amount
            v-bind:amount="costsTotalWithoutFee"
          />
        </v-flex>
      </v-layout>

      <v-layout>
        <v-flex />
        <v-flex
          class="text-xs-right"
        >
          <base-display-amount
            v-bind:amount="fee"
          />
        </v-flex>
      </v-layout>

      <hr>

      <v-layout>
        <v-flex />
        <v-flex
          class="text-xs-right"
        >
          <base-display-amount
            v-bind:amount="costsTotalWithFee"
          />
        </v-flex>
      </v-layout>
      <hr>
      <hr>
    </v-flex>
  </v-layout>
</template>

<script>
import BaseDisplayAmount from '../../base-display-amount';

export default {
  name: 'OverviewCosts',
  components: { BaseDisplayAmount },
  props: {
    costsTotalWithFee: {
      required: true,
      type: Number,
    },
    costsTotalWithoutFee: {
      required: true,
      type: Number,
    },
  },
  computed: {
    fee() {
      return this.costsTotalWithFee - this.costsTotalWithoutFee;
    },
  },
};
</script>

<style scoped>

</style>
