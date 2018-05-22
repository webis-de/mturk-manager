<template>
<div class="headline">
	Current balance:
	<component-display-money v-if="balance != undefined" v-bind:amount="balance"></component-display-money>
	<v-tooltip top>
        <v-btn flat icon small v-bind:loading="show_spinner" v-on:click="update_balance_custom" slot="activator" class="ma-0">
          <v-icon>refresh</v-icon>
        </v-btn>
      	<span>Refresh current balance</span>
    </v-tooltip>
</div>
</template>

<script>
    import ComponentDisplayMoney from './component-display-money.vue';
    import { mapState, mapActions } from 'vuex';
export default {
    name: 'component-show-balance',
    data () {
        return {
        	updating: false,
        }
    },
    computed: {
    	show_spinner: function() {
    		return this.updating || this.balance == undefined;
    	},
        // ...mapGetters('moduleMoney', ['balance']),
        ...mapState('moduleMoney', ['balance']),
    },
    methods: {
    	update_balance_custom: function() {
    		this.updating = true;
    		
    		this.update_balance().then((result) => {
    			this.updating = false;
    		});
    	},
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
    // watch: {
    // 	balance: function() {
    // 		this.updating = false;
    // 	}
    // },
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