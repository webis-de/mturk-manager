<template>
  <div class="subheading">
    Current balance:
    <base-display-amount
      v-if="get_balance() !== null"
      v-bind:amount="parseInt(get_balance() * 100)"
    ></base-display-amount>
    <v-progress-circular
      v-else
      indeterminate
      size="20"
      width="2"
    ></v-progress-circular>
    <!--<v-tooltip top>-->
    <!--<v-btn flat icon small v-bind:loading="show_spinner" v-on:click="update_balance_custom" slot="activator" class="ma-0">-->
    <!--<v-icon>refresh</v-icon>-->
    <!--</v-btn>-->
    <!--<span>Refresh current balance</span>-->
    <!--</v-tooltip>-->
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import BaseDisplayAmount from '../base-display-amount';

export default {
  name: 'ComponentShowBalance',
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
  methods: {
    // update_balance_custom: function() {
    // 	this.updating = true;
    //
    // 	this.update_balance(true).then((result) => {
    // 		this.updating = false;
    // 	});
    // },
    // ...mapActions('module_finances', {
    // 	'update_balance': 'update_balance',
    // }),
  },
  components: {
    BaseDisplayAmount,
  },
};
</script>

<style lang="scss" scoped></style>
