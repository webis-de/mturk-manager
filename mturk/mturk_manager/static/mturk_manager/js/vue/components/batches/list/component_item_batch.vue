<template>
    <!-- <div>wda</div> -->
    <tr
        v-bind:key="batch.id"
    >
        <td>
            <v-checkbox
                v-model="props.selected"
                primary
                hide-details
            ></v-checkbox>
        </td>
        <td 
            class="text-xs-center"
        >
            {{ batch.name }}
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
        v-on:click="foo()"
            class="text-xs-center"
        >
            {{ Object.keys(batch.object_hits).length }}
        </td>
        <td 
            class="text-xs-center"
        >
            {{ batch.settings_batch.count_assignments }}
        </td>
        <td 
            class="text-xs-center"
        >
            <component-progress
                slot="activator"
                v-bind:progress="batch.progress"
            >
                {{ batch.count_assignments_available }}/{{batch.count_assignments_total}} assignment{{batch.count_assignments_total > 1 ? 's' : ''}}
            </component-progress>
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
                        id_batch: batch.id, 
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
    import ComponentProgress from './component_progress.vue';
    import ComponentDisplayDatetime from '../../helpers/component_display_datetime.vue';
    import Batch from '../../../classes/batch.js';
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
        batch() {
            console.log('calculated batch')
            return this.props.item;
        },
        ...mapGetters(['get_show_progress_indicator']),
    },
    methods: {
    },
    mounted(){
    },
    components: {
        ComponentProgress,
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