import { mapState, mapActions, mapGetters } from 'vuex';

export default {
	methods: {
	    refresh_data() {
	    	console.log(this.use_sandbox)
	        this.set_show_progress_indicator(true);
	        // this.set_show_progress_indicator(true);

	        // this.sync_database().then(() => {
	        //     this.set_show_progress_indicator(false);
	        // });

	        this.sync_batches(true).then(() => {
	            this.set_show_progress_indicator(false);
	        });
	        
	        // this.update_balance().then(() => {
	        //     this.set_show_progress_indicator(false);
	        // });
	    },
        ...mapActions(['set_show_progress_indicator']),
        ...mapActions('moduleBatches', {
            'sync_batches': 'sync_batches', 
        }),
	},
	computed: {
        ...mapState(['use_sandbox']),
	},
 	created() {
        this.refresh_data();
	},
    watch: {
        use_sandbox: function() {
            this.refresh_data();
        },
    },
}