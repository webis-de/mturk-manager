<template>

    <v-dialog v-model="show_dialog" max-width="800px" persistent>
            <v-btn slot="activator" v-bind:disabled="is_disabled" v-on:click="policy_to_be_edited = null" color="error" dark class="mb-2">
                <v-icon>delete</v-icon>{{ title_button }}
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
                        </v-container>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" flat v-on:click.native="cancel">Cancel</v-btn>
                        <v-btn color="red darken-1" flat v-on:click.native="remove">Delete</v-btn>
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
            this.delete_qualifications(this.qualifications_selected).then(() => {
                // this.show_dialog = false;
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