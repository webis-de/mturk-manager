<template>
    <v-dialog v-bind:disabled="is_disabled" v-model="show_dialog" max-width="800px" persistent>
            <v-btn slot="activator" v-bind:disabled="is_disabled" color="error" class="mb-2">
                <v-icon left>delete</v-icon>{{ title_button }}
            </v-btn>

            <v-card>
                    <v-card-title>
                        <span class="headline">{{ title_dialog }}</span>
                    </v-card-title>
                    <v-card-text>
                        <v-container grid-list-md>
                            <v-layout wrap>
                                <v-flex xs12>
                                    Do you really want to delete the following qualification(s)?
                                </v-flex>
                            </v-layout>
                            <v-layout wrap>
                                <v-flex xs12>
                                    <v-list dense >
                                        <v-list-tile v-for="(qualification, index) in qualifications_selected" :key="qualification.id_mturk">
                                            <v-list-tile-content>
                                                <v-list-tile-title>{{ qualification.display_name() }}</v-list-tile-title>
                                            </v-list-tile-content>
                                        </v-list-tile>
                                    </v-list>
                                </v-flex>
                            </v-layout>
                        </v-container>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" flat v-bind:disabled="is_deleting" v-on:click.native="cancel">Cancel</v-btn>
                        <v-btn color="red darken-1" v-bind:loading="is_deleting" flat v-on:click.native="remove">Delete</v-btn>
                    </v-card-actions>
            </v-card>
    </v-dialog>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    // import { Policy } from '../../store/modules/policies.js';
    import { Qualification } from '../../classes/qualifications.js';
    
    // import ComponentShowBalance from './component-show-balance.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'component-delete-qualification',
    props: {
        qualifications_selected: {
            type: Array,
            required: true,
        }
    },
    data () {
        return {
            show_dialog: false,
            is_deleting: false,
            title_dialog: 'Delete Qualification(s)',
        }
    },
    computed: {
        is_disabled: function() {
            return this.qualifications_selected.length == 0;
        },
        title_button: function() {
            return `delete ${this.qualifications_selected.length} Qualification(s)`;
        }
    },
    methods: {
        remove: function() {
            this.is_deleting = true;
            this.delete_qualifications(this.qualifications_selected).then(() => {
                this.show_dialog = false;
                this.is_deleting = false;
            });
        },
        cancel: function() {
            this.show_dialog = false;
        },
        ...mapActions('moduleQualifications', {
            'delete_qualifications': 'delete_qualifications',
        }),
    },
    watch: {
    }
}
</script>