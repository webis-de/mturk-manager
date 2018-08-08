<template>
        <span>
            <v-layout>
                <v-flex xs1>
                    <v-switch label="Not Blocked" v-model="show_workers_blocked_none"></v-switch>
                </v-flex>
                <v-flex xs1>
                    <v-switch label="Soft Blocked" v-model="show_workers_blocked_soft"></v-switch>
                </v-flex>
                <v-flex xs1>
                    <v-switch label="Hard Blocked" v-model="show_workers_blocked_hard"></v-switch>
                </v-flex>
            
                <v-flex>
                    <v-text-field
                        v-model="search"
                        append-icon="search"
                        label="Search for name"
                        hide-details
                        class="mb-2"
                    ></v-text-field>
                </v-flex>

            </v-layout>
        <!-- <v-divider></v-divider> -->

            <!-- <v-container grid-list-md fluid> -->
            <v-data-iterator
                v-bind:items="list_workers"
                v-bind:rows-per-page-items="items_per_page"
                content-tag="v-layout"
                row
                wrap
                v-bind:search="search"
                v-bind:custom-filter="custom_filter"
                select-all
            >
                <!-- v-bind:filter="custom" -->
                <!-- item-key="is_blocked" -->
                <v-flex
                    slot="item"
                    slot-scope="props"
                    xs3
                >
                    <component-item-worker
                        v-bind:worker="props.item"
                    >
                        <!-- content-tag="v-flex" -->
                    </component-item-worker>
                </v-flex>
            </v-data-iterator>
        <!-- </v-container> -->
    </span>
    <!-- </v-layout> -->


    <!-- <v-data-table
        v-bind:items="list_workers"
        v-bind:headers="list_headers"
        disable-initial-sort
        v-bind:pagination.sync="pagination"
        v-model="workers_selected"
        select-all
        item-key="name"
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
            <td class="justify-end layout">
                <v-btn icon class="mx-0" v-on:click="init_edit_policy(props.item)">
                    <v-icon color="teal">edit</v-icon>
                </v-btn>
                <v-btn icon class="mx-0" v-on:click="delete_policy(props.item)">
                    <v-icon color="pink">delete</v-icon>
                </v-btn>
            </td>
        </template>
    </v-data-table> -->
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    // import { Policy } from '../../store/modules/policies.js';
    import { STATUS_BLOCK } from '../../classes/enums.js';
    
    import ComponentItemWorker from './component_item_worker.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'component-list-workers',
    data () {
        return {
            workers_selected: [],

            show_dialog_policy: false,
            policy_to_be_edited: null,

            items_per_page: [12, 24],

            search: '',

            show_workers_blocked_none: true,
            show_workers_blocked_soft: true,
            show_workers_blocked_hard: true,

            // search: 'A10BOAO1EONNS7',
            // policy_new: new Policy({
            //     QualificationTypeStatus: 'Active',
            // }),
        }
    },
    computed: {
        // policy_dialog: function() {
        //     return this.policy_to_be_edited == null ? this.policy_new : this.policy_to_be_edited;
        // },
        // title_dialog_policy: function() {
        //     return this.policy_to_be_edited == null ? 'New Policy' : 'Edit Policy';
        // },
        ...mapGetters('moduleWorkers', {
            'list_workers': 'list_workers',
        }),
    },
    methods: {
        custom_filter(items, search, filter) {
            if(!this.show_workers_blocked_none)
            {
                items = items.filter(e => e.is_blocked != STATUS_BLOCK.NONE);
            }
            if(!this.show_workers_blocked_soft)
            {
                items = items.filter(e => e.is_blocked != STATUS_BLOCK.SOFT);
            }
            if(!this.show_workers_blocked_hard)
            {
                items = items.filter(e => e.is_blocked != STATUS_BLOCK.HARD);
            }


            // console.log(items)
            search = search.trim()
            if(search != '')
            {
                items = items.filter(e => filter(e.name, search));
                
            }
            // console.log(filter)
            return items
        },
        // custom(object, search) {
        //     console.log(object)
        //     console.log(search)
        //     return true
        // },
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
    },
    created: function() {
    },

    components: {
        ComponentItemWorker,
    },
}
</script>