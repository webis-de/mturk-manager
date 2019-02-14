<template>
    <tr
        v-bind:key="hit.id"
        v-on:click="props.expanded = !props.expanded"
        class="text-no-wrap"
    >
        <td v-bind:style="stylesCell">
            <v-checkbox
                v-model="is_selected"
                primary
                hide-details
            ></v-checkbox>
        </td>
        <td
            v-if="set_columns_selected.has('id_hit')"
            class="text-xs-center"
            v-bind:style="stylesCell"
        >
            {{ hit.id_hit }}
        </td>
        <td
            v-if="set_columns_selected.has('batch')"
            class="text-xs-center"
            v-bind:style="stylesCell"
        >
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
            v-if="set_columns_selected.has('datetime_creation')"
            class="text-xs-center"
            v-bind:style="stylesCell"
        >
            <component-display-datetime
                v-bind:datetime="hit.datetime_creation"
            ></component-display-datetime>
        </td>
        <td
            v-if="set_columns_selected.has('progress')"
            class="text-xs-center"
            v-bind:style="stylesCell"
        >
            <component-batch-progress
                v-bind:progress="hit.progress"
            >
                {{ hit.count_assignments_available }}/{{hit.count_assignments_total}} assignment{{hit.count_assignments_total > 1 ? 's' : ''}}
            </component-batch-progress>
        </td>
        <td
            class="text-xs-center"
            v-if="show_links === true && set_columns_selected.has('actions')"
            v-bind:style="stylesCell"
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
    import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
    import ComponentBatchProgress from '../../batches/list/component_batch_progress.vue';
    import _ from 'lodash';
    import ComponentDisplayDatetime from "../../helpers/component_display_datetime";

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
        array_columns_selected: {
            type: Array,
            required: true,
        },

        isCondensed: {
            required: true,
            type: Boolean,
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
        set_columns_selected() {
            return new Set(this.array_columns_selected);
        },
        is_selected: {
            get() {
                return _.has(this.object_hits_selected, this.hit.id);
            },
            set(is_selected) {
                this.set_hits_selected({
                    array_items: [this.hit],
                    add: is_selected,
                });
            }
        },
        ...mapGetters('moduleHITs', {
            'object_hits_selected': 'get_object_hits_selected',
        }),
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
        stylesCell() {
            if(this.isCondensed) {
                return {
                    height: 'unset !important',
                    paddingLeft: '5px !important',
                    paddingRight: '5px !important',
                }
            } else {
                return {}
            }
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
        ...mapMutations('moduleHITs', {
            'set_hits_selected': 'set_hits_selected',
        }),
    },
    components: {
        ComponentDisplayDatetime,
        ComponentBatchProgress,
    },
}
</script>

<style lang="scss" scoped>
</style>