<template>
    <!-- <div>wda</div> -->
    <tr
        v-bind:key="batch.id"
    >
        <td>
            <v-checkbox
                v-model="is_selected"
                primary
                hide-details
            ></v-checkbox>
        </td>

        <td 
            class="text-xs-center"
        >
            {{ batch.name.toUpperCase() }}
        </td>

        <td 
        v-on:click="foo()"
            class="text-xs-center"
        >
            {{ batch.count_hits }}
        </td>

        <td 
            class="text-xs-center"
        >
            <component-display-datetime
                v-bind:datetime="batch.datetime_creation"
            >
            </component-display-datetime>
        </td>

        <td
            class="text-xs-center"
        >
            {{ batch.settings_batch.count_assignments }}
        </td>

        <td
            class="text-xs-center"
        >
            <component-display-money v-bind:amount="batch.settings_batch.reward"></component-display-money>
        </td>

        <td
            class="text-xs-center"
        >
            {{ batch.count_assignments_total }}
        </td>

        <td
            class="text-xs-center"
        >
            {{ batch.count_assignments_approved }}
        </td>

        <td
            class="text-xs-center"
        >
            {{ batch.count_assignments_rejected }}
        </td>

        <td
            class="text-xs-center"
        >
            {{ batch.costs_max }}
        </td>

        <td 
            class="text-xs-center"
        >
            <component-batch-progress
                slot="activator"
                v-bind:progress="batch.progress"
            >
                {{ batch.count_assignments_available }}/{{batch.count_assignments_total}} assignment{{batch.count_assignments_total > 1 ? 's' : ''}}
            </component-batch-progress>
        </td>
        
        <td 
            class="text-xs-center"
        >
            <v-btn
                slot="activator" 
                class="my-0"
                icon
                small
                v-bind:to="{
                    name: 'batch', 
                    params: { 
                        slug_project: $route.params.slug_project, 
                        id_batch: batch.id
                    } 
                }"
            >
                <v-icon>info</v-icon>
            </v-btn>
        </td>
    </tr>
</template>
<script>
    import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
    import _ from 'lodash';
    import ComponentBatchProgress from './component_batch_progress.vue';
    import ComponentDisplayDatetime from '../../helpers/component_display_datetime.vue';
    import Batch from '../../../classes/batch.js';
    import ComponentDisplayMoney from "../../component-display-money";
export default {
    name: 'component-item-batch',
    props: {
        props: {
            required: true,
        },
    },
    data () {
        return {
        }
    },
    computed: {
        is_selected: {
            get() {
                return _.has(this.object_batches_selected, this.batch.id);
            },
            set(is_selected) {
                this.set_batches_selected({
                    array_items: [this.batch],
                    add: is_selected,
                });
            }
        },
        batch() {
            return this.props.item;
        },
        ...mapGetters(['get_show_progress_indicator']),
        ...mapGetters('moduleBatches', {
            'object_batches_selected': 'get_object_batches_selected',
        }),
    },
    methods: {
        ...mapMutations('moduleBatches', {
            'set_batches_selected': 'set_batches_selected',
        }),
    },
    mounted(){
    },
    components: {
        ComponentDisplayMoney,
        ComponentBatchProgress,
        ComponentDisplayDatetime,
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