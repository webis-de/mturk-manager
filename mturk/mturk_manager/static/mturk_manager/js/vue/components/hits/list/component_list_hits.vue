<template>
<v-layout wrap>
    <v-flex>
        <!-- {{list_batches}} -->
        <h1 class="headline">HITs</h1>
        <v-data-table
            select-all
            v-bind:pagination.sync="pagination"
            v-bind:headers="list_headers"
            v-bind:items="list_hits_processed"
            v-bind:search="search"
            v-model="hits_selected"
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
                            v-on:click.native="hits_selected = toggleAll(hits_selected, list_hits_processed)"
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
                <component-item-hit
                    v-bind:props="props"
                    v-bind:show_links="show_links"
                >
                </component-item-hit>
            </template>
        </v-data-table>
        <!-- {{list_workers}} -->
    </v-flex>
</v-layout>
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    // import { Policy } from '../../store/modules/policies.js';
    import ComponentItemHit from './component_item_hit.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
    import table from '../../../mixins/table';
export default {
    mixins: [
        table,
    ],
    name: 'component-list-hits',
    props: {
        list_hits: {
            required: false,
            type: Array,
        },
        show_links: {
            required: false,
            type: Boolean,
            default: true,
        },
    },
    data () {
        return {
            hits_selected: [],
            pagination: { rowsPerPage: 25 },

            search: '',

            // search: 'A10BOAO1EONNS7',
            // policy_new: new Policy({
            //     QualificationTypeStatus: 'Active',
            // }),

        }
    },
    computed: {
        list_headers() {
            const list_headers = [
                {
                    text: 'Name',
                    value: 'id_hit',
                },
                {
                    text: 'Batch',
                    value: 'batch',
                },
                {
                    text: 'Progress',
                    value: 'progress',
                    align: 'center',
                },
            ];

            if(this.show_links == true) {
                list_headers.push({
                    text: '',
                    value: '',
                });
            }

            return list_headers;
        },
        list_hits_processed() {
            if(this.list_hits != undefined)
            {
                return this.list_hits;
            } else {
                return this.list_hits_all;
            }
        },
        // ...mapGetters('moduleProjects', {
        //     'project_current': 'get_project_current',
        // }),
        ...mapGetters('moduleHITs', {
            'list_hits_all': 'list_hits',
        }),
    },
    methods: {
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
        ComponentItemHit,
    },
}
</script>

<style lang="scss" scoped>
    #row_header {
        height: 48px;
    }
</style>