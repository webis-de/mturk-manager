<template>
<v-layout wrap>
    <v-flex>
        <v-layout>
            <v-flex>
                <!-- {{list_batches}} -->
                <h1 class="headline">Assignments</h1>
            </v-flex>
        </v-layout>
        <v-layout>
            <v-flex class="shrink" mr-3>
                <v-switch label="Only Submitted" v-model="filters.show_only_submitted_assignments"></v-switch>
            </v-flex>
            <v-flex>
                <v-text-field
                    append-icon="search"
                    label="Filter by worker"
                    hide-details
                    v-model="filters.worker"
                    class="mb-2"
                ></v-text-field>
            </v-flex>
        </v-layout>
        <v-layout>
            <v-flex>
                <v-data-table
                    select-all
                    v-bind:headers="list_headers"
                    v-bind:items="array_assignments_prepared"
                    v-bind:pagination.sync="pagination"
                    v-bind:total-items="items_total"
                    v-bind:input="assignments_selected_local"
                    v-bind:loading="loading"
                    item-key="id"
                    class="my-3"
                >
                    <template slot="headers" slot-scope="props">
                        <tr id="row_header">
                            <th>
                                    <!--v-bind:input-value="props.all"-->
                                    <!--v-bind:indeterminate="props.indeterminate"-->
                                <v-checkbox
                                    v-bind:input-value="is_page_selected(array_assignments_prepared, object_assignments_selected)"
                                    primary
                                    hide-details
                                    v-on:click.native="batches_selected = toggle_all(
                                        array_assignments_prepared,
                                        set_assignments_selected,
                                        object_assignments_selected
                                    )"
                                ></v-checkbox>
                            </th>
                            <th
                                v-for="header in props.headers"
                                v-bind:key="header.value"
                                v-bind:width="header.width"
                                v-bind:class="[
                                    'column',
                                    header.sortable === false ? '' : 'sortable',
                                    pagination.descending ? 'desc' : 'asc',
                                    header.value === pagination.sortBy ? 'active' : ''
                                ]"
                                v-on="header.sortable != false ? {click: () => {pagination.sortBy = header.value; pagination.descending = !pagination.descending}} : {}"
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
                        <component-item-assignment
                            v-bind:props="props"
                            v-bind:show_links="show_links"
                        ></component-item-assignment>
                    </template>
                </v-data-table>
            </v-flex>
        </v-layout>
    </v-flex>
</v-layout>
</template>
<script>
    import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
    // import { Policy } from '../../store/modules/policies.js';
    import ComponentItemAssignment from './component_item_assignment.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
    import {table} from '../../../mixins/table';
    import {STATUS_EXTERNAL} from "../../../classes/enums";
    import {update_sandbox} from "../../../mixins/update_sandbox";
    import {external_pagination} from "../../../mixins/external_pagination";
    import {Service_Assignments} from "../../../services/service_assignments";
export default {
    mixins: [
        update_sandbox,
        external_pagination,
        table,
    ],
    name: 'component-list-assignments',
    props: {
        id_hit: {
            required: false,
            type: Number,
        },
        show_links: {
            required: false,
            type: Boolean,
            default: true,
        },
    },
    data () {
        return {
            // assignments_selected: [],
            pagination: { rowsPerPage: 25, sortBy: 'datetime_creation', descending: true },
            filters: {
                show_only_submitted_assignments: false,
                worker: '',
            },
            items_total: undefined,
            loading: false,
            // search: 'A10BOAO1EONNS7',
            // policy_new: new Policy({
            //     QualificationTypeStatus: 'Active',
            // }),

        }
    },
    beforeDestroy() {
        this.clear_assignments_selected();
    },
    computed: {
    	assignments_selected_local: {
    		get() {
    			return this.assignments_selected;
    		},
    		set(value) {
    			this.set_assignments_selected(value);
    		},
    	},
        array_assignments_prepared() {
            let array_assignments_prepared = undefined;
            if(this.use_sandbox === true)
            {
                array_assignments_prepared = this.array_assignments_sandbox;
            } else {
                array_assignments_prepared = this.array_assignments;
            }

            if(array_assignments_prepared === null) {
                return [];
            }

            return array_assignments_prepared;
        },
        ...mapGetters('moduleAssignments', {
            'array_assignments': 'get_array_assignments',
            'array_assignments_sandbox': 'get_array_assignments_sandbox',
            'object_assignments_selected': 'get_object_assignments_selected',
        }),
        list_headers() {
            const list_headers = [
                {
                    text: 'Name',
                    value: 'id_assignment',
                },
                {
                    text: 'Creation',
                    value: 'datetime_creation',
                },
                {
                    text: 'Worker',
                    value: 'worker',
                    align: 'center',
                },
                {
                    text: 'Status',
                },
                {
                    text: 'HIT',
                    value: 'hit',
                },
            ];

            // if(this.show_links == true) {
            //     list_headers.push({
            //         text: 'Link',
            //         value: '',
            //     });
            // }

            return list_headers;
        },
        list_assignments_processed() {
            if(this.list_assignments != undefined)
            {
                return this.list_assignments;
            } else {
                return this.list_assignments_all;
            }
        },
        // ...mapGetters('moduleProjects', {
        //     'project_current': 'get_project_current',
        // }),
        ...mapGetters('moduleAssignments', {
            'list_assignments_all': 'list_assignments',
            'assignments_selected': 'get_array_assignments_selected',
        }),
    },
    methods: {
        load_page() {
            this.loading = true;
            Service_Assignments.load_page(this.pagination, {
                id_hit: this.id_hit,
                ...this.filters,
            }).then((items_total) => {
                this.items_total = items_total;
                this.loading = false;
            });
        },
        ...mapMutations('moduleAssignments', {
            'set_assignments_selected': 'set_assignments_selected',
            'clear_assignments_selected': 'clear_assignments_selected',
        }),
    },
    created: function() {
    },

    components: {
        ComponentItemAssignment,
    },
}
</script>

<style lang="scss" scoped>
    #row_header {
        height: 48px;
    }
</style>