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
                v-bind:id_hit="id_hit"
        ></component-list-assignments>
    </v-flex>
</v-layout>
    
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import ComponentListAssignments from '../../assignments/list/component_list_assignments.vue';
    import _ from 'lodash';
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
        list_assignments() {
            if(this.hit.object_assignments == undefined)
            {
                return [];
            } else {
                return _.orderBy(this.hit.object_assignments);
            }
        },
        hit() {
            const object_hits = this.get_object_hits();
            if(object_hits == null) {
                return {};
            } else {
                if(object_hits[this.id_hit] == undefined)
                {
                    return {};
                } else {
                    return object_hits[this.id_hit];
                }
            }
        },
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