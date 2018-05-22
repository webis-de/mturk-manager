<template>
<div class="display-1">
	Current balance:
	<template v-if="balance == undefined">
		<v-progress-circular
			indeterminate
		></v-progress-circular>
	</template>
	<template v-else>
		<component-display-money v-bind:amount="balance"></component-display-money>
		<v-tooltip top>
	        <v-btn flat icon v-bind:loading="updating" v-on:click="update_balance_custom" slot="activator">
	          <v-icon>refresh</v-icon>
	        </v-btn>
          	<span>Refresh current balance</span>
	    </v-tooltip>
	</template>
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