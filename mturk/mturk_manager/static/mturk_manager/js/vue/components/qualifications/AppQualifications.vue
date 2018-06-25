<template>
<div>
    <v-layout wrap>
        <v-flex>
            <!-- {{list_policies}} -->

            <v-data-table
                v-bind:items="list_policies"
                v-bind:headers="list_headers"
                disable-initial-sort
                v-model="policies_selected"
                item-key="id_mturk"
                select-all
                class="elevation-1"
            >
                 <template slot="items" slot-scope="props">
                    <td>
                        <v-checkbox
                            v-model="props.selected"
                            primary
                            hide-details
                        ></v-checkbox>
                    </td>
                    <td>{{ props.item.display_name() }}</td>
                    <td>{{ props.item.display_description() }}</td>
                    <td>{{ props.item.created_at.toLocaleString() }}</td>
                    <td class="justify-end layout">
                        <v-tooltip left>
                            <v-btn v-if="!props.item.has_database_entry()" icon class="mx-0" slot="activator">
                                <v-icon color="warning">warning</v-icon>
                            </v-btn>
                            <span>No database entry for this qualification was found!</span>
                         </v-tooltip>
                        <v-btn icon class="mx-0" v-on:click="qualification_to_be_edited = props.item">
                            <v-icon color="success">edit</v-icon>
                        </v-btn>
                        <!-- <v-btn icon class="mx-0" v-on:click="delete_policy(props.item)">
                            <v-icon color="error">delete</v-icon>
                        </v-btn> -->
                    </td>
                </template>
            </v-data-table>
        </v-flex>
    </v-layout>

    <v-layout wrap>
        <component-add-qualification
        ></component-add-qualification>

        <component-delete-qualification
            v-bind:qualifications_selected="policies_selected"
        ></component-delete-qualification>

        <component-update-qualification
            v-bind:qualification_to_be_edited="qualification_to_be_edited"
            v-on:finished="qualification_to_be_edited = undefined"
        ></component-update-qualification>

        <component-download-qualifications
            v-bind:qualifications_selected="policies_selected"
        ></component-download-qualifications>
    </v-layout>
</div>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import { Qualification } from '../../classes/qualifications.js';
	
    import ComponentAddQualification from './component-add-qualification.vue';
    import ComponentDeleteQualification from './component-delete-qualification.vue';
    import ComponentUpdateQualification from './component-update-qualification.vue';
    import ComponentDownloadQualifications from './component-download-qualifications.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'app-qualifications',

    data () {
        return {
            policies_selected: [],
            list_headers: [
                {
                    text: 'Name',
                    value: 'name_mturk',
                },
                {
                    text: 'Description',
                    value: 'description_mturk',
                },
                {
                    text: 'Created At',
                    value: 'created_at',
                },
                { 
                    text: '', 
                    // text: 'Actions', 
                    value: 'name', 
                    sortable: false,
                    align: 'right'
                }
            ],

            qualification_to_be_edited: undefined,
        }
    },
    watch: {
        list_policies: function() {
            this.set_show_progress_indicator(true);

            this.sync_qualifications().then(() => {
                this.set_show_progress_indicator(false);
            });
            console.log("dwadaw");
        },
    },
    computed: {
        ...mapGetters('moduleQualifications', {
            'list_policies': 'list_policies',
        }),
    },
    methods: {
        delete_policy(item) {
            // if(confirm(`Do you really want to delete the '${item.name}' policy?`))
            // {

            // }
        },
        edit_policy() {
            this.update_policy(this.policy_dialog).then(() => {
            });
        },
        ...mapActions('moduleQualifications', {
            'sync_qualifications': 'sync_qualifications',
            'update_policy': 'update_policy',
        }),
        ...mapActions(['set_show_progress_indicator']),
    },
    created: function() {
        this.set_show_progress_indicator(true);

        this.sync_qualifications().then(() => {
            this.set_show_progress_indicator(false);
        });
    },

    components: {
        ComponentAddQualification,
        ComponentDeleteQualification,
        ComponentUpdateQualification,
        ComponentDownloadQualifications,
     // ComponentShowMoneySpent,
     // ComponentShowBatches,
    },
}
</script>