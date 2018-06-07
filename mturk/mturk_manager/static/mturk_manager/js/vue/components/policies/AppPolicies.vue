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
                    <td>{{ props.item.name }}</td>
                    <td>{{ props.item.description }}</td>
                    <td class="justify-end layout">
                        <v-btn icon class="mx-0" v-on:click="init_edit_policy(props.item)">
                            <v-icon color="teal">edit</v-icon>
                        </v-btn>
                        <v-btn icon class="mx-0" v-on:click="delete_policy(props.item)">
                            <v-icon color="pink">delete</v-icon>
                        </v-btn>
                    </td>
                </template>
            </v-data-table>
        </v-flex>
    </v-layout>
    <v-dialog v-model="show_dialog_policy" max-width="800px" persistent>
        <v-btn slot="activator" v-on:click="policy_to_be_edited = null" color="primary" dark class="mb-2">New Policy</v-btn>
        <v-card>
            <v-card-title>
              <span class="headline">{{ title_dialog_policy }}</span>
            </v-card-title>
            <v-card-text>
              <v-container grid-list-md>
                <v-layout wrap>
                  <v-flex xs12>
                    <v-text-field v-model="policy_dialog.name" label="Name"></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field v-model="policy_dialog.description" label="Description"></v-text-field>
                  </v-flex>
                  <v-flex xs12 sm6 md4>
                    <v-text-field v-model="policy_dialog.is_requestable" label="Is Requestable"></v-text-field>
                  </v-flex>
                  <v-flex xs12 sm6 md4>
                    <v-text-field v-model="policy_dialog.status" label="Status"></v-text-field>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" flat v-on:click.native="cancel">Cancel</v-btn>
              <v-btn color="blue darken-1" flat v-on:click.native="add_or_edit_policy">Save</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</div>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import { Policy } from '../../store/modules/policies.js';
	
    // import ComponentShowBalance from './component-show-balance.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'app-finances',

    data () {
        return {
            policies_selected: [],
            list_headers: [
                {
                    text: 'Name',
                    value: 'name',
                },
                {
                    text: 'Description',
                    value: 'description',
                },
                { 
                    text: 
                    'Actions', 
                    value: 'name', 
                    sortable: false,
                    align: 'right'
                }
            ],

            show_dialog_policy: false,
            policy_to_be_edited: null,
            policy_new: new Policy({
                QualificationTypeStatus: 'Active',
            }),
        }
    },
    computed: {
        policy_dialog: function() {
            return this.policy_to_be_edited == null ? this.policy_new : this.policy_to_be_edited;
        },
        title_dialog_policy: function() {
            return this.policy_to_be_edited == null ? 'New Policy' : 'Edit Policy';
        },
        ...mapGetters('modulePolicies', {
            'list_policies': 'list_policies',
        }),
    },
    methods: {
        add_or_edit_policy() {
            if(this.policy_to_be_edited == null)
            {
                this.add_policy_custom();
            } else {
                this.edit_policy();
            }
        },
        delete_policy(item) {
            if(confirm(`Do you really want to delete the '${item.name}' policy?`))
            {

            }
        },
        init_edit_policy(policy_to_be_edited) {
            this.policy_to_be_edited = policy_to_be_edited;
            this.show_dialog_policy = true;
        },
        edit_policy() {
            this.update_policy(this.policy_dialog).then(() => {
                this.show_dialog_policy = false;
            });
        },
        add_policy_custom() {
            this.add_policy(this.policy_dialog).then(() => {
                this.show_dialog_policy = false;
            });
        },
        cancel() {
            this.show_dialog_policy = false;
        },
        ...mapActions('modulePolicies', {
            'sync_policies': 'sync_policies',
            'add_policy': 'add_policy',
            'update_policy': 'update_policy',
        }),
        ...mapActions(['set_show_progress_indicator']),
    },
    created: function() {
        this.set_show_progress_indicator(true);

        this.sync_policies().then(() => {
            this.set_show_progress_indicator(false);
        });
    },

    components: {
     // ComponentShowBalance,
     // ComponentShowMoneySpent,
     // ComponentShowBatches,
    },
}
</script>