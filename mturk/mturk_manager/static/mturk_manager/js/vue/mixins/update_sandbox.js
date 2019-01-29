import { mapState, mapActions } from 'vuex';

export const update_sandbox =  {
	methods: {
        ...mapActions(['set_show_progress_indicator']),
	},
	computed: {
        ...mapState('module_app', ['use_sandbox']),
	},
    watch: {
        use_sandbox: function(use_sandbox) {
            this.sandbox_updated(use_sandbox);
        },
    },
}