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
        ></component-list-hits>
	</v-flex>
</v-layout>
    
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
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
        }
    },
    // watch: {
    //     'worker.is_blocked': function() {
    //         console.log(this.worker.is_blocked)
    //     },
    // },
    computed: {
        list_hits() {
            if(this.batch.object_hits == undefined)
            {
                return [];
            } else {
                return _.orderBy(this.batch.object_hits);
            }
        },
    	batch() {
    		const object_batches = this.get_object_batches();
    		if(object_batches == null) {
    			return {}
    		} else {
                if(object_batches[this.id_batch] == undefined)
                {
                    return {};
                } else {
                    return object_batches[this.id_batch];
                }
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
        ...mapGetters('moduleBatches', {
            'get_object_batches': 'get_object_batches',
        }),
        ...mapGetters(['get_show_progress_indicator']),
    },
    created: function () {
        Service_Batches.get_batch(this.id_batch);
    },
    methods: {
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