<template>
    <!-- <div>wda</div> -->

<v-layout wrap>
    <v-flex>
    	<!-- {{object_batches}} -->
        <h2 class="headline">
        	Batch {{batch.name}}
            <v-btn
                slot="activator" 
                class="my-0"
                icon
                small
                v-bind:to="{name: 'batches'}"
            >
                <v-icon>arrow_upward</v-icon>
            </v-btn>
        </h2>
        <v-divider class="my-3"></v-divider>
        <component-list-hits
            v-bind:id_batch="id_batch"

            v-bind:array_columns_selected="array_columns_selected"
            v-bind:array_columns_selected_initial="array_columns_selected_initial"
            v-bind:function_reset_array_columns="function_reset_array_columns"
            v-bind:function_set_array_columns="function_set_array_columns"
        ></component-list-hits>
	</v-flex>
</v-layout>
    
</template>
<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import ComponentListHits from '../../hits/list/component_list_hits.vue';
    import _ from 'lodash';
    import {Service_Batches} from "../../../services/service_batches";

export default {
    name: 'component-batch-detail',
    // props: {
    // 	id_batch: {
    // 		required: true,
    // 	},
    // },
    props: {
    	id_batch: {
    		required: true,
    		type: Number,
    	}
    },
    data () {
        return {
            batch_intern: undefined,
        }
    },
    // watch: {
    //     'worker.is_blocked': function() {
    //         console.log(this.worker.is_blocked)
    //     },
    // },
    computed: {
        // list_hits() {
        //     if(this.batch.object_hits == undefined)
        //     {
        //         return [];
        //     } else {
        //         return _.orderBy(this.batch.object_hits);
        //     }
        // },
    	batch() {
    	    return this.batch_intern === undefined ? {} : this.batch_intern;
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
        // ...mapGetters('moduleBatches', {
        //     'get_object_batches': 'get_object_batches',
        // }),
        ...mapGetters('moduleHITs', {
            'array_columns_selected': 'get_array_columns_selected_general',
            'array_columns_selected_initial': 'get_array_columns_selected_initial_general',
        }),
        ...mapGetters(['get_show_progress_indicator']),
    },
    created: function () {
        Service_Batches.get_batch(this.id_batch).then((batch) => {
            this.batch_intern = batch;
        });
    },
    methods: {
        ...mapActions('moduleHITs', {
            'function_reset_array_columns': 'reset_array_columns_general',
        }),
        ...mapMutations('moduleHITs', {
            'function_set_array_columns': 'set_array_columns_general'
        }),
    },
    components: {
        ComponentListHits,
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