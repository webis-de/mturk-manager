<template>
<v-layout wrap>
    <v-flex>
        <!-- {{list_batches}} -->
       	<h1 class="headline">Assignments</h1>
        <v-data-table
            select-all
            v-bind:pagination.sync="pagination"
            v-bind:headers="list_headers"
            v-bind:items="list_assignments_processed"
            v-bind:search="search"
            v-model="assignments_selected_local"
            item-key="id"
            class="my-3"
        >
            <template slot="headers" slot-scope="props">
                <tr id="row_header">
                    <th>
                        <v-checkbox
                            v-bind:input-value="props.all"
                            v-bind:indeterminate="props.indeterminate"
                            primary
                            hide-details
                            v-on:click.native="assignments_selected_local = toggleAll(assignments_selected_local, list_assignments_processed)"
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
                <component-item-assignment
                    v-bind:props="props"
                    v-bind:show_links="show_links"
                ></component-item-assignment>
            </template>
        </v-data-table>
        <!-- {{list_workers}} -->
    </v-flex>
</v-layout>
</template>
<script>
    import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
    // import { Policy } from '../../store/modules/policies.js';
    import ComponentItemAssignment from './component_item_assignment.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
    import table from '../../../mixins/table';
export default {
    mixins: [
        table,
    ],
    name: 'component-list-assignments',
    props: {
        list_assignments: {
            required: false,
            type: Array|undefined,
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
            pagination: { rowsPerPage: 25 },

            search: '',

            // search: 'A10BOAO1EONNS7',
            // policy_new: new Policy({
            //     QualificationTypeStatus: 'Active',
            // }),

        }
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
        }),
        ...mapState('moduleAssignments', {
            'assignments_selected': 'assignments_selected',
        }),
    },
    methods: {
        ...mapMutations('moduleAssignments', {
            'set_assignments_selected': 'set_assignments_selected',
        }),
        // ...mapActions('moduleWorkers', {
            // 'update_status_block': 'update_status_block',
        // }),
    },
    created: function() {

            // this.update_status_block({
            //     worker: {name: 'A7W013PM199BS'},
            //     status_block_new: 1,
            //     status_block_old: 2,
            // });
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