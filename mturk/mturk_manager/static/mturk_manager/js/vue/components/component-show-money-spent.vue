<template>
<span>
    <span class="headline">
        Max costs:
        <component-display-money v-bind:amount="money_spent_max"></component-display-money>
    </span>
    <span class="subheading">
        (costs so far:
        <component-display-money v-bind:amount="money_spent"></component-display-money>)
    </span>
</span>
</template>

<script>
    import { mapState, mapGetters, mapActions } from 'vuex';
    import ComponentDisplayMoney from './component-display-money.vue';
    import _ from 'lodash';
export default {
    name: 'component-show-money-spent',
    data () {
        return {
        	updating: false,
        }
    },
    computed: {
        money_spent: function() {
            if(this.show_with_fee) {
                return _.sumBy(this.list_batches, 'money_spent_with_fee');
            } else {
                return _.sumBy(this.list_batches, 'money_spent_without_fee');
            }
        },
        money_spent_max: function() {
            if(this.show_with_fee) {
                return _.sumBy(this.list_batches, 'money_spent_max_with_fee');
            } else {
                return _.sumBy(this.list_batches, 'money_spent_max_without_fee');
            }
        },
        ...mapGetters(['list_batches']),
        ...mapState(['show_with_fee']),
    },
    methods: {
        ...mapActions('moduleMoney', {
        	'update_balance': 'update_balance'
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
        ComponentDisplayMoney,
    },
}
</script>

<style lang="scss" scoped>
</style>