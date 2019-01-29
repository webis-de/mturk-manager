import { mapState, mapActions, mapGetters } from 'vuex';
import {Service_Batches} from "../services/service_batches";

export default {
	methods: {
	    refresh_data(force=false) {
	    	// console.log(this.use_sandbox)
	        this.set_show_progress_indicator(true);
	        // this.set_show_progress_indicator(true);

	        // this.sync_database().then(() => {
	        //     this.set_show_progress_indicator(false);
	        // });
			Service_Batches.load_batches(force).then(() => {
	            this.set_show_progress_indicator(false);
			});
	        
	        // this.update_balance().then(() => {
	        //     this.set_show_progress_indicator(false);
	        // });
	    },
        ...mapActions(['set_show_progress_indicator']),
	},
	computed: {
        ...mapState('module_app', ['use_sandbox']),
	},
 	created() {
        this.refresh_data(false);
	},
    watch: {
        use_sandbox: function() {
            this.refresh_data(false);
        },
    },
}