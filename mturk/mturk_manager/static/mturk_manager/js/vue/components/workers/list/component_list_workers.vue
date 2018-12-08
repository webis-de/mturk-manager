<template>
        <span>
            <v-layout>
                <v-flex>
                    <v-layout>
                        <!--<v-flex class="shrink" mr-3>-->
                            <!--<v-switch label="Not Blocked" v-model="filters.show_workers_blocked_none"></v-switch>-->
                        <!--</v-flex>-->
                        <!--<v-flex class="shrink" mr-3>-->
                            <!--<v-switch label="Limit Blocked" v-model="filters.show_workers_blocked_limit"></v-switch>-->
                        <!--</v-flex>-->
                        <!--<v-flex class="shrink" mr-3>-->
                            <!--<v-switch label="Project Blocked" v-model="filters.show_workers_blocked_soft"></v-switch>-->
                        <!--</v-flex>-->
                        <!--<v-flex class="shrink" mr-3>-->
                            <!--<v-switch label="Global Blocked" v-model="filters.show_workers_blocked_hard"></v-switch>-->
                        <!--</v-flex>-->
                    </v-layout>
                </v-flex>
                
                <v-flex>
                    <v-layout>
                        <v-flex>
                            <v-text-field
                                v-model="filters.id_worker"
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
                <!--v-bind:search="search"-->
            <v-data-table
                    select-all
                v-bind:headers="list_headers"
                v-bind:items="array_workers_prepared"
                v-bind:pagination.sync="pagination"
                v-bind:total-items="items_total"
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
    import _ from 'lodash';
    import ComponentItemWorker from './component_item_worker.vue';
    import {Service_Workers} from "../../../services/service_worker";
    import {update_sandbox} from "../../../mixins/update_sandbox";
    import {external_pagination} from "../../../mixins/external_pagination";
    import {table} from "../../../mixins/table";
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    mixins: [
        update_sandbox,
        external_pagination,
        table,
    ],
    name: 'component-list-workers',
    data () {
        return {
            workers_selected: [],
            pagination: { rowsPerPage: 5 },
            // pagination: { rowsPerPage: 5, totalItems: 30 },
            show_dialog_policy: false,
            policy_to_be_edited: null,


            items_total: undefined,
            // items_per_page: [12, 24],

            filters: {
                id_worker: '',
                show_workers_blocked_none: true,
                show_workers_blocked_limit: true,
                show_workers_blocked_soft: true,
                show_workers_blocked_hard: true,
            },

            // search: 'A10BOAO1EONNS7',
            // policy_new: new Policy({
            //     QualificationTypeStatus: 'Active',
            // }),

            list_headers: [
                {
                    text: 'Name',
                    value: 'name',
                },
                
                // {
                //     text: 'Approved (%)',
                //     value: 'percentage_approved_assignments',
                //     align: 'center',
                //     width: '1px'
                // },
                // {
                //     text: 'Rejected (%)',
                //     value: 'percentage_rejected_assignments',
                //     align: 'center',
                //     width: '1px'
                // },
                
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
        array_workers_prepared() {
            let array_workers_prepared = undefined;
            if(this.use_sandbox === true)
            {
                array_workers_prepared = this.array_workers_sandbox;
            } else {
                array_workers_prepared = this.array_workers;
            }

            if(array_workers_prepared === null) {
                return [];
            }

            return array_workers_prepared;
        },
        ...mapGetters('moduleWorkers', {
            'array_workers': 'get_array_workers',
            'array_workers_sandbox': 'get_array_workers_sandbox',
        }),
        list_workers() {
            return this.list_workers_processed.slice(0, 5)
        },
        // policy_dialog: function() {
        //     return this.policy_to_be_edited == null ? this.policy_new : this.policy_to_be_edited;
        // },
        // title_dialog_policy: function() {
        //     return this.policy_to_be_edited == null ? 'New Policy' : 'Edit Policy';
        // },
        ...mapGetters('moduleWorkers', {
            'list_workers_processed': 'list_workers',
        }),
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
    },
    methods: {
        load_page() {
            this.loading = true;
            Service_Workers.load_page(this.pagination, {
                ...this.filters,
            }).then((items_total) => {
                this.items_total = items_total;
                this.loading = false;
            });
        },
        // custom_filter(items, search, filter) {
        //     if(!this.show_workers_blocked_none)
        //     {
        //         items = items.filter(e => !e.is_blocked_soft && !e.is_blocked_hard);
        //     }
        //     if(!this.show_workers_blocked_limit)
        //     {
        //         items = items.filter(e => e.count_assignments_limit >= this.project_current.count_assignments_max_per_worker);
        //     }
        //     if(!this.show_workers_blocked_soft)
        //     {
        //         items = items.filter(e => e.is_blocked_soft);
        //     }
        //     if(!this.show_workers_blocked_hard)
        //     {
        //         items = items.filter(e => e.is_blocked_hard);
        //     }
        //
        //     search = search.trim()
        //     if(search != '')
        //     {
        //         items = items.filter(e => filter(e.id_worker, search));
        //
        //     }
        //     // console.log(filter)
        //     return items
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