<template>
        <span>
            <v-layout>
                <v-flex>
                    <v-layout>
                        <v-flex class="shrink" mr-3>
                            <v-switch label="Not Blocked" v-model="show_workers_blocked_none"></v-switch>
                        </v-flex>
                        <v-flex class="shrink" mr-3>
                            <v-switch label="Limit Blocked" v-model="show_workers_blocked_limit"></v-switch>
                        </v-flex>
                        <v-flex class="shrink" mr-3>
                            <v-switch label="Project Blocked" v-model="show_workers_blocked_soft"></v-switch>
                        </v-flex>
                        <v-flex class="shrink" mr-3>
                            <v-switch label="Global Blocked" v-model="show_workers_blocked_hard"></v-switch>
                        </v-flex>
                    </v-layout>
                </v-flex>
                
                <v-flex>
                    <v-layout>
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
                </v-flex>

            </v-layout>

                <!-- select-all -->
                <!-- v-bind:rows-per-page-items="items_per_page" -->
            <v-data-table
                select-all
                v-bind:pagination.sync="pagination"
                v-bind:headers="list_headers"
                v-bind:items="list_workers"
                v-bind:search="search"
                v-bind:custom-filter="custom_filter"
                v-model="workers_selected"
            >
                <template slot="headers" slot-scope="props">
                    <tr class="row_header">
                        <th>
                            <v-checkbox
                                v-bind::input-value="props.all"
                                v-bind::indeterminate="props.indeterminate"
                                primary
                                hide-details
                                v-on:click.native="toggleAll"
                            ></v-checkbox>
                        </th>
                        <th
                            v-for="header in props.headers"
                            v-bind:key="header.value"
                            v-bind:width="header.width"
                            v-bind:class="[
                                'column sortable', 
                                pagination.descending ? 'desc' : 'asc', 
                                header.value === pagination.sortBy ? 'active' : ''
                            ]"
                            v-on:click="changeSort(header.value)"
                        >
                            <v-icon small>arrow_upward</v-icon>
                            {{ header.text }}
                        </th>
                    </tr>
                </template>

                <template
                    slot="items"
                    slot-scope="props"
                >
                    <component-item-worker
                        v-bind:props="props"
                    >
                    </component-item-worker>
                </template>
            </v-data-table>
            <!-- {{list_workers}} -->
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
    import { STATUS_BLOCK } from '../../../classes/enums.js';
    
    import ComponentItemWorker from './component_item_worker.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'component-list-workers',
    data () {
        return {
            workers_selected: [],
            pagination: { rowsPerPage:-1 },
            show_dialog_policy: false,
            policy_to_be_edited: null,

            // items_per_page: [12, 24],

            search: '',

            show_workers_blocked_none: true,
            show_workers_blocked_limit: true,
            show_workers_blocked_soft: true,
            show_workers_blocked_hard: true,

            // search: 'A10BOAO1EONNS7',
            // policy_new: new Policy({
            //     QualificationTypeStatus: 'Active',
            // }),

            list_headers: [
                {
                    text: 'Name',
                    value: 'name',
                },
                
                {
                    text: 'Approved (%)',
                    value: 'percentage_approved_assignments',
                    align: 'center',
                    width: '1px'
                },
                {
                    text: 'Rejected (%)',
                    value: 'percentage_rejected_assignments',
                    align: 'center',
                    width: '1px'
                },
                
                {
                    text: 'Assignment Limit',
                    value: 'counter_assignments',
                    align: 'center',
                    width: '1px'
                },
                {
                    text: 'Project Block',
                    value: 'block_soft',
                    width: '1px'
                },
                {
                    text: 'Soft MTurk Block',
                    value: 'block_soft_hard',
                    width: '1px'
                },
                {
                    text: 'Hard MTurk Block',
                    value: 'block_hard',
                    width: '1px'
                },
            ],
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
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
    },
    methods: {
        // toggleAll () {
        //     if (this.workers_selected.length) this.workers_selected = []
        //     else this.workers_selected = this.list_workers.slice()
        // },
        // changeSort (column) {
        //     if (this.pagination.sortBy === column) 
        //     {
        //         this.pagination.descending = !this.pagination.descending;
        //     } else {
        //         this.pagination.sortBy = column;
        //         this.pagination.descending = false;
        //     }
        // },
        custom_filter(items, search, filter) {
            if(!this.show_workers_blocked_none)
            {
                items = items.filter(e => !e.is_blocked_soft && !e.is_blocked_hard);
            }
            if(!this.show_workers_blocked_limit)
            {
                items = items.filter(e => e.count_assignments_limit >= this.project_current.count_assignments_max_per_worker);
            }
            if(!this.show_workers_blocked_soft)
            {
                items = items.filter(e => e.is_blocked_soft);
            }
            if(!this.show_workers_blocked_hard)
            {
                items = items.filter(e => e.is_blocked_hard);
            }

            search = search.trim()
            if(search != '')
            {
                items = items.filter(e => filter(e.id_worker, search));
                
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
        ...mapActions('moduleWorkers', {
            'update_status_block': 'update_status_block',
        }),
    },
    created: function() {
            // this.update_status_block({
            //     worker: {name: 'A7W013PM199BS'},
            //     status_block_new: 1,
            //     status_block_old: 2,
            // });
    },

    components: {
        ComponentItemWorker,
    },
}
</script>

<style lang="scss" scoped>
    .row_header {
        height: 48px;
        // height: unset !important;
    }
</style>