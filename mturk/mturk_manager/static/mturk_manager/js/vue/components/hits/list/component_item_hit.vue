<template>
    <!-- <div>wda</div> -->
    <tr 
        v-bind:key="hit.id"
        v-on:click="props.expanded = !props.expanded"
    >
        <td>
            <v-checkbox
                v-model="props.selected"
                primary
                hide-details
            ></v-checkbox>
        </td>
        <td class="text-xs-center">
            {{ hit.id_hit }}
        </td>
        <td class="text-xs-center">
            {{ hit.batch.name.toUpperCase() }}
            <v-btn
                slot="activator"
                class="my-0"
                icon
                small
                v-bind:to="{
                    name: 'batch',
                    params: {
                        slug_project: $route.params.slug_project,
                        id_batch: hit.batch.id,
                    }
                }"
            >
                <v-icon>info</v-icon>
            </v-btn>
        </td>
        <td 
            class="text-xs-center"
        >
            <component-progress
                slot="activator"
                v-bind:progress="hit.progress"
            >
                {{ hit.count_assignments_available }}/{{hit.count_assignments_total}} assignment{{hit.count_assignments_total > 1 ? 's' : ''}}
            </component-progress>
        </td>
        <td 
            class="text-xs-center"
            v-if="show_links == true"
        >
            <v-btn
                slot="activator"
                class="my-0"
                icon
                small
                v-bind:to="{
                    name: 'hit',
                    params: {
                        slug_project: $route.params.slug_project,
                        id_hit: hit.id,
                    }
                }"
            >
                <v-icon>info</v-icon>
            </v-btn>
        </td>
        <!-- <td class="text-xs-center">
            {{ hit.hits.length }}
        </td>
        <td class="text-xs-center">
            {{ hit.count_assignments }}
        </td> -->
    </tr>
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import ComponentProgress from '../../batches/list/component_progress.vue';
    import _ from 'lodash';

export default {
    name: 'component-item-hit',
    props: {
        props: {
            type: Object,
            required: true,
        },
        show_links: {
            required: false,
            type: Boolean,
            default: true,
        },
    },
    data () {
        return {
        }
    },
    // watch: {
    //     'worker.is_blocked': function() {
    //         console.log(this.worker.is_blocked)
    //     },
    // },
    computed: {
        // count_assignments_total() {
        //     return this.hit.batch.settings_batch.count_assignments;
        // },
        count_assignments() {
            return _.size(this.hit.assignments);
        },
        // progress() {
        //     console.log('EXECUTED')
        //     return (this.count_assignments_available / this.count_assignments_total) * 100.0;
        // },
        hit() {
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
        ComponentProgress,
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