<template>
    <!-- <div>wda</div> -->
    <tr 
        v-bind:key="assignment.id"
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
            {{ assignment.id_assignment }}
        </td>
        <td 
            class="text-xs-center"
        >
            {{ assignment.worker.id_worker }}
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
            v-if="show_links == true"
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
    import { mapState, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';

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
        assignment() {
        	// console.log(this.props.item)
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