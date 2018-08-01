<template>
<div>
    <!-- <v-layout wrap> -->
        <!-- <v-flex> -->
        <component-list-workers>
        </component-list-workers>
        <!-- </v-flex> -->
    <!-- </v-layout> -->
</div>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    // import { Policy } from '../../store/modules/policies.js';
	
    import ComponentListWorkers from './component_list_workers.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'app-finances',

    data () {
        return {
        	workers_selected: [],
		    pagination: {
		      rowsPerPage: 10,
		    },
            list_headers: [
                {
                    text: 'Name',
                    value: 'name',
                },
            ],

            show_dialog_policy: false,
            policy_to_be_edited: null,
            // policy_new: new Policy({
            //     QualificationTypeStatus: 'Active',
            // }),
        }
    },
    watch: {
        use_sandbox: function() {
            this.refresh_data();
        },
    },
    computed: {
        // policy_dialog: function() {
        //     return this.policy_to_be_edited == null ? this.policy_new : this.policy_to_be_edited;
        // },
        // title_dialog_policy: function() {
        //     return this.policy_to_be_edited == null ? 'New Policy' : 'Edit Policy';
        // },
        // ...mapGetters('moduleWorkers', {
        //     'list_workers': 'list_workers',
        // }),
        ...mapState(['use_sandbox']),
    },
    methods: {
        refresh_data() {
            this.set_show_progress_indicator(true);

            this.sync_workers().then(() => {
                this.set_show_progress_indicator(false);
            });
        },
        // add_or_edit_policy() {
        //     if(this.policy_to_be_edited == null)
        //     {
        //         this.add_policy_custom();
        //     } else {
        //         this.edit_policy();
        //     }
        // },
        // delete_policy(item) {
        //     if(confirm(`Do you really want to delete the '${item.get_name()}' policy?`))
        //     {

        //     }
        // },
        // init_edit_policy(policy_to_be_edited) {
        //     this.policy_to_be_edited = policy_to_be_edited;
        //     this.show_dialog_policy = true;
        // },
        // edit_policy() {
        //     this.update_policy(this.policy_dialog).then(() => {
        //         this.show_dialog_policy = false;
        //     });
        // },
        // add_policy_custom() {
        //     this.add_policy(this.policy_dialog).then(() => {
        //         this.show_dialog_policy = false;
        //     });
        // },
        // cancel() {
        //     this.show_dialog_policy = false;
        // },
        ...mapActions('moduleWorkers', {
            'sync_workers': 'sync_workers',
        }),
        ...mapActions(['set_show_progress_indicator']),
    },
    created: function() {
        this.refresh_data();
    },

    components: {
     ComponentListWorkers,
     // ComponentShowMoneySpent,
     // ComponentShowBatches,
    },
}
</script>