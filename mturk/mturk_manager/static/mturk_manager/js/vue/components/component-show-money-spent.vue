<template>
<div class="headline">
	Spent money:
    <template>
        <component-display-money v-bind:amount="money_spent"></component-display-money>
    </template>
</div>
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
            return _.sumBy(this.list_batches, 'money_spent');
        },
        ...mapGetters(['list_batches']),
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