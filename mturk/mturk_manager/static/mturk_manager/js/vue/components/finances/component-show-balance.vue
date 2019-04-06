<template>
  <div class="subheading">
    <!--Current balance:-->
    <base-display-amount
      v-if="get_balance() !== null"
      v-bind:amount="parseInt(get_balance() * 100)"
    />
    <v-progress-circular
      v-else
      indeterminate
      size="20"
      width="2"
    />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import BaseDisplayAmount from '../base-display-amount';

export default {
  name: 'ComponentShowBalance',
  components: {
    BaseDisplayAmount,
  },
  data() {
    return {
      updating: false,
    };
  },
  computed: {
    show_spinner() {
      return this.updating || this.get_balance === undefined;
    },
    ...mapGetters('module_finances', {
      get_balance: 'get_balance',
    }),
  },
};
</script>

<style lang="scss" scoped></style>
