<template>
<div class="headline">
	Current balance:
	<component-display-money
        v-if="get_balance !== null"
        v-bind:amount="get_balance() * 100"
    ></component-display-money>
	<!--<v-tooltip top>-->
        <!--<v-btn flat icon small v-bind:loading="show_spinner" v-on:click="update_balance_custom" slot="activator" class="ma-0">-->
          <!--<v-icon>refresh</v-icon>-->
        <!--</v-btn>-->
      	<!--<span>Refresh current balance</span>-->
    <!--</v-tooltip>-->
</div>
</template>

<script>
    import ComponentDisplayMoney from './../component-display-money.vue';
    import { mapState, mapActions, mapGetters } from 'vuex';
export default {
    name: 'component-show-balance',
    data () {
        return {
        	updating: false,
        }
    },
    computed: {
    	show_spinner: function() {
    		return this.updating || this.get_balance === undefined;
    	},
        ...mapGetters('module_finances', {
            'get_balance': 'get_balance',
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
    	ComponentDisplayMoney,
    },
}
</script>

<style lang="scss" scoped>
</style>