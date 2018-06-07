<template>
<div>
    <v-layout wrap>
        <v-flex xs12 md6>
            <component-show-money-spent></component-show-money-spent>
        </v-flex>

        <v-flex xs12 md6 text-md-right>
            <component-show-balance></component-show-balance>
        </v-flex>
    </v-layout>
    <v-divider class="my-3"></v-divider>
    <div style="max-width: 100%">
        <!-- <v-flex> -->
            <component-show-batches></component-show-batches>
        <!-- </v-flex> -->
    </div>
</div>
</template>

<script>
    import { mapState, mapActions } from 'vuex';
	
    import ComponentShowBalance from './component-show-balance.vue';
    import ComponentShowMoneySpent from './component-show-money-spent.vue';
    import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'app-finances',

    data () {
        return {
            dialog: false,

            drawer: false,
            is_refreshing: true,
            show_snackbar: false,
            text_snackbar: 'Finished refreshing the data',
        }
    },
    methods: {
        ...mapActions(['set_show_progress_indicator']),
        ...mapActions('moduleBatches', {
        	'sync_database': 'sync_database', 
        }),
        ...mapActions('moduleMoney', {
        	'update_balance': 'update_balance'
        }),
    },
    created: function() {
        this.set_show_progress_indicator(true);
        let count_loaded = '0';

    	this.sync_database().then(() => {
    		if(++count_loaded == 2) 
    		{
        		this.set_show_progress_indicator(false);
    		}
    	});
    	
    	this.update_balance().then(() => {
    		if(++count_loaded == 2) 
    		{
        		this.set_show_progress_indicator(false);
    		}
    	});
    },

    components: {
     ComponentShowBalance,
     ComponentShowMoneySpent,
     ComponentShowBatches,
    },
}
</script>