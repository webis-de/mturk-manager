<template>
<v-layout wrap>
    <v-flex>
        <!-- {{list_batches}} -->
        <h1 class="headline">HITs</h1>
        <v-data-table
            select-all
            v-bind:pagination.sync="pagination"
            v-bind:headers="list_headers"
            v-bind:items="array_hits_prepared"
            v-bind:search="search"
            v-bind:total-items="items_total"
            v-model="hits_selected"
            item-key="id"
            class="my-3"
            v-bind:loading="loading"
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
    import {table} from '../../../mixins/table';
    import {update_sandbox} from "../../../mixins/update_sandbox";
    import {external_pagination} from "../../../mixins/external_pagination";
    import {Service_HITs} from "../../../services/service_hits";
    import Batch from "../../../classes/batch";
export default {
    mixins: [
        update_sandbox,
        external_pagination,
        table,
    ],
    name: 'component-list-hits',
    props: {
        id_batch: {
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
            hits_selected: [],
            pagination: { rowsPerPage: 25, sortBy: 'datetime_creation', descending: true },

            search: '',

            items_total: undefined,

            loading: false,

            // search: 'A10BOAO1EONNS7',
            // policy_new: new Policy({
            //     QualificationTypeStatus: 'Active',
            // }),

        }
    },
    computed: {
        array_hits_prepared() {
            let array_hits_current = undefined;
            if(this.use_sandbox === true)
            {
                array_hits_current = this.array_hits_sandbox;
            } else {
                array_hits_current = this.array_hits;
            }

            if(array_hits_current === null) {
                return [];
            }

            return array_hits_current;
        },
        list_headers() {
            const list_headers = [
                {
                    text: 'ID',
                    value: 'id_hit',
                },
                {
                    text: 'Batch',
                    value: 'batch',
                },
                {
                    text: 'Creation',
                    value: 'datetime_creation',
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
            return [];
        },
        // ...mapGetters('moduleProjects', {
        //     'project_current': 'get_project_current',
        // }),
        ...mapGetters('moduleHITs', {
            'list_hits_all': 'list_hits',
            'array_hits': 'get_array_hits',
            'array_hits_sandbox': 'get_array_hits_sandbox',
        }),
    },
    methods: {
        load_page() {
            this.loading = true;
            Service_HITs.load_page(this.pagination, {
                id_batch: this.id_batch,
            }).then((items_total) => {
                this.items_total = items_total;
                this.loading = false;
            });
        },
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