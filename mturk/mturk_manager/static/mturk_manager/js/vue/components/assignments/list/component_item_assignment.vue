<template>
    <!-- <div>wda</div> -->
    <tr 
        v-bind:key="assignment.id"
        v-on:click="props.expanded = !props.expanded"
    >
        <td>
            <v-checkbox
                v-model="is_selected"
                primary
                hide-details
            ></v-checkbox>
        </td>
        <td class="text-xs-center">
            {{ assignment.id_assignment }}
        </td>
        <td class="text-xs-center">
            <component-display-datetime v-bind:datetime="assignment.datetime_creation"></component-display-datetime>
        </td>
        <td 
            class="text-xs-center"
        >
            {{ assignment.worker.id_worker }}
        </td>
        <td class="text-xs-center">
            <component-status-assignment
                v-bind:assignment="assignment"
            ></component-status-assignment>
        </td>
        <td class="text-xs-center">{{ assignment.hit.id_hit }}
            <v-btn
                slot="activator" 
                class="my-0"
                icon
                small
                v-bind:to="{
                    name: 'hit',
                    params: {
                        slug_project: $route.params.slug_project, 
                        id_hit: assignment.hit.id,
                    }
                }"
            >
                <v-icon>info</v-icon>
            </v-btn>
        </td>
        <td 
            class="text-xs-center"
            v-if="show_links == false"
        >
            <v-btn
                slot="activator" 
                class="my-0"
                icon
                small
                v-bind:to="{
                    name: 'assignment', 
                    params: { 
                        slug_project: $route.params.slug_project, 
                        id_assignment: assignment.id, 
                    } 
                }"
            >
                <v-icon>info</v-icon>
            </v-btn>
        </td>
        <!-- <td class="text-xs-center">
            {{ assignment.hits.length }}
        </td>
        <td class="text-xs-center">
            {{ props.item.count_assignments }}
        </td> -->
    </tr>
</template>
<script>
    import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
    import _ from 'lodash';
    import ComponentDisplayDatetime from "../../helpers/component_display_datetime";
    import ComponentStatusAssignment from "./component-status-assignment";

export default {
    name: 'component-item-assignment',
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
        is_selected: {
            get() {
                return _.has(this.object_assignments_selected, this.assignment.id);
            },
            set(is_selected) {
                this.set_assignments_selected({
                    array_items: [this.assignment],
                    add: is_selected,
                });
            }
        },
        assignment() {
            return this.props.item;
        },
        ...mapGetters('moduleAssignments', {
            'object_assignments_selected': 'get_object_assignments_selected',
        }),
        ...mapGetters(['get_show_progress_indicator']),
    },
    methods: {
        ...mapMutations('moduleAssignments', {
            'set_assignments_selected': 'set_assignments_selected',
        }),
    },
    components: {
        ComponentStatusAssignment,
        ComponentDisplayDatetime
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