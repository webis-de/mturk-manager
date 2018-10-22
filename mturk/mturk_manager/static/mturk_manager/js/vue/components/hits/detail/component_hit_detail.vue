<template>
    <!-- <div>wda</div> -->

<v-layout wrap>
    <v-flex>
        <!-- {{object_batches}} -->
        <h2 class="headline">
            HIT {{hit.id_hit}}
            <v-btn
                slot="activator" 
                class="my-0"
                icon
                small
                v-bind:to="{name: 'hits'}"
            >
                <v-icon>arrow_upward</v-icon>
            </v-btn>
        </h2>
        <v-divider class="my-3"></v-divider>
        <component-list-assignments
            v-bind:list_assignments="hit.assignments"
        ></component-list-assignments>
    </v-flex>
</v-layout>
    
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import ComponentListAssignments from '../../assignments/list/component_list_assignments.vue';

export default {
    name: 'component-hit-detail',
    // props: {
    //  id_hit: {
    //      required: true,
    //  },
    // },
    props: {
        id_hit: {
            required: true,
            type: Number
        }
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
        hit() {
            const object_hits = this.get_object_hits();
            if(object_hits == null) {
                return {}
            } else {
                return object_hits[this.id_hit];
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
        ...mapGetters('moduleHITs', {
            'get_object_hits': 'get_object_hits',
        }),
        ...mapGetters(['get_show_progress_indicator']),
    },
    methods: {
    },
    components: {
        ComponentListAssignments,
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