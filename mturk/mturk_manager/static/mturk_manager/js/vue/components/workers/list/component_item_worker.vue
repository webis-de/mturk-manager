<template>
    <!-- <div>wda</div> -->
    <tr>
        <td>
            <v-checkbox
                v-model="props.selected"
                primary
                hide-details
            ></v-checkbox>
        </td>
        <td
            v-if="set_columns_selected.has('name')"
            class="text-xs-left"
        >
            {{ props.item.id_worker }}
        </td>
        <!--<td>-->
        <!--</td>-->
        <!--<td>-->
        <!--</td>-->
        <td
            v-if="set_columns_selected.has('counter_assignments')"
            class="text-xs-center"
        >
            <component-limit-assignments
                v-bind:key="`component_limit_assignments_${props.item.name}`"
                v-bind:worker="worker"
            ></component-limit-assignments>
        </td>
        <td
            v-if="set_columns_selected.has('block_soft')"
            class="text-xs-center"
        >
            <component-block-soft-worker
                v-bind:key="`component_block_soft_worker_${worker.name}`"
                v-bind:worker="worker"
            ></component-block-soft-worker>
        </td>
        <td
            v-if="set_columns_selected.has('block_soft_hard')"
            class="text-xs-center"
        >
            <component-block-global-worker
                v-bind:key="`component_block_global_worker_${worker.name}`"
                v-bind:worker="worker"
            ></component-block-global-worker>
        </td>
        <td
            v-if="set_columns_selected.has('block_hard')"
            class="text-xs-center"
        >
            <component-block-hard-worker
                v-bind:key="`component_block_hard_worker_${worker.name}`"
                v-bind:worker="worker"
            ></component-block-hard-worker>
        </td>
    </tr>
    <!-- <v-card class="ma-1">
        <v-card-title
            class="py-0"
        >
            <h4>{{ worker.name }}</h4>
            <v-spacer></v-spacer>
            <v-menu 
                bottom 
                left
                v-bind:close-on-content-click="false"

            >
                <v-btn
                    slot="activator"
                    dark
                    icon
                     class="ma-0"
                >
                    <v-icon>more_vert</v-icon>
                </v-btn>

                <v-list>
                    <v-list-tile
                    >
                        <component-block-worker
                            v-bind:key="`component_block_worker_${worker.name}`"
                            v-bind:worker="worker"
                        ></component-block-worker>
                    </v-list-tile>

                </v-list>
            </v-menu>
        </v-card-title>
        <v-divider></v-divider>
        <v-list dense>
            <v-list-tile>
                <v-list-tile-content>Block Status:</v-list-tile-content>
                <v-list-tile-content class="align-end">

                    <v-tooltip left>
                        <v-btn icon v-bind:loading="status_block.icon == ''" slot="activator" class="ma-0">
                            <v-icon v-bind:color="status_block.color">{{ status_block.icon }}</v-icon>
                        </v-btn>
                        <span>{{ status_block.description }}</span>
                    </v-tooltip>
                </v-list-tile-content>
            </v-list-tile>
            <v-list-tile>
                <v-list-tile-content>#Assignments:</v-list-tile-content>
                <v-list-tile-content class="align-end">
                    <v-text-field
                        type="number"
                        v-bind:loading="get_show_progress_indicator"
                        single-line
                        v-bind:value="worker.counter_assignments"
                        v-on:change="changed_counter_assignments($event)"
                        v-bind:suffix="`of ${project_current.count_assignments_max_per_worker}`"
                    ></v-text-field>
                </v-list-tile-content>
            </v-list-tile>
        </v-list>

        <v-snackbar
            v-model="show_snackbar"
            v-bind:timeout="1500"
            bottom
        >
            Saved!
            <v-btn
                flat
                v-on:click="show_snackbar = false"
            >
                Close
            </v-btn>
        </v-snackbar>
    </v-card> -->
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import { STATUS_BLOCK } from '../../../classes/enums.js';

    import ComponentBlockWorker from './component_block_worker.vue';
    // import ComponentBlockSoftWorker from './component_block_worker.vue';
    import ComponentBlockSoftWorker from './component_block_soft_worker.vue';
    import ComponentBlockGlobalWorker from './component_block_global_worker.vue';
    import ComponentBlockHardWorker from './component_block_hard_worker.vue';
    import ComponentLimitAssignments from './component_limit_assignments.vue';
export default {
    name: 'component-item-worker',
    props: {
        props: {
            type: Object,
            required: true,
        },
        array_columns_selected: {
            type: Array,
            required: true,
        },
    },
    data () {
        return {
            show_snackbar: false,
        }
    },
    // watch: {
    //     'worker.is_blocked': function() {
    //         console.log(this.worker.is_blocked)
    //     },
    // },
    computed: {
        set_columns_selected() {
            return new Set(this.array_columns_selected);
        },
        worker() {
            return this.props.item;
        },
        // status_block() {
        //     if(this.worker.is_blocked == undefined)
        //     {
        //         return {
        //             description: 'Loading',
        //             color: 'success',
        //             icon: '',
        //         };
        //     }

        //     switch(this.worker.is_blocked)
        //     {
        //         case STATUS_BLOCK.NONE:
        //             return {
        //                 description: 'Not Blocked',
        //                 color: 'success',
        //                 icon: 'check',
        //             };
        //         case STATUS_BLOCK.SOFT:
        //             return {
        //                 description: 'Soft Blocked',
        //                 color: 'warning',
        //                 icon: 'block',
        //             };
        //         case STATUS_BLOCK.HARD:
        //             return {
        //                 description: 'Hard Blocked',
        //                 color: 'error',
        //                 icon: 'block',
        //             };
        //     }
        // },
        ...mapGetters(['get_show_progress_indicator']),
    },
    methods: {
    },
    components: {
        ComponentBlockSoftWorker,
        ComponentBlockGlobalWorker,
        ComponentBlockHardWorker,
        ComponentLimitAssignments,
    },
}
</script>

<style lang="scss" scoped>
    td {
        height: unset !important;
    }
    td .v-input--selection-controls {
        padding: unset;
    }
</style>