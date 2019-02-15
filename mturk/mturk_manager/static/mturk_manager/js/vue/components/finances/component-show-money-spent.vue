<template>
  <span>
    <span class="headline">
      Max costs:
      <base-display-amount
        v-bind:amount="money_spent_max"
      ></base-display-amount>
    </span>
    <!-- <v-runtime-template :template="template"></v-runtime-template> -->
    <span class="subheading">
      (costs so far:
      <base-display-amount v-bind:amount="money_spent"></base-display-amount>)
    </span>
    <span class="subheading">
      (money not spent:
      <base-display-amount v-bind:amount="money_not_spent"></base-display-amount
      >)
    </span>
  </span>
</template>

<script>
import Vue from 'vue';
import VRuntimeTemplate from 'v-runtime-template';
import { mapState, mapGetters, mapActions } from 'vuex';
import _ from 'lodash';
import BaseDisplayAmount from '../base-display-amount.vue';

export default {
  name: 'component-show-money-spent',
  data() {
    return {
      updating: true,
      template: '<div><div>Hello {{ updating }}!</div><div>Hello {{ updating }}!</div></div>',
    };
  },
  created() {},
  mounted() {
    console.log('started');
    console.log('finished');
  },
  computed: {
    tmp() {
      this.list_batches;
    },
    money_spent() {
      if (this.show_with_fee) {
        return _.sumBy(this.list_batches, 'money_spent_with_fee');
      }
      return _.sumBy(this.list_batches, 'money_spent_without_fee');
    },
    money_not_spent() {
      if (this.show_with_fee) {
        return _.sumBy(this.list_batches, 'money_not_spent_with_fee');
      }
      return _.sumBy(this.list_batches, 'money_not_spent_without_fee');
    },
    money_spent_max() {
      if (this.show_with_fee) {
        return _.sumBy(this.list_batches, 'money_spent_max_with_fee');
      }
      return _.sumBy(this.list_batches, 'money_spent_max_without_fee');
    },
    ...mapGetters('moduleBatches', {
      list_batches: 'list_batches',
    }),
    ...mapState(['show_with_fee']),
  },
  methods: {
    ...mapActions('moduleMoney', {
      update_balance: 'update_balance',
    }),
    //     load_config: function() {
    //         const configElement = document.getElementById( 'config' );
    //         const config = JSON.parse( configElement.innerHTML );
    //         console.log(config);
    //         this.url_api_get_balance = config.url_api_get_balance;
    //     },
  },
  // created: function() {
  //     this.load_config();
  //     console.log(this.balance);
  //     // this.store.dispatch('refresh_balance');
  //     this.update_balance();
  // },
  components: {
    ComponentDisplayMoney: BaseDisplayAmount,
    VRuntimeTemplate,
  },
};
</script>

<style lang="scss" scoped></style>
