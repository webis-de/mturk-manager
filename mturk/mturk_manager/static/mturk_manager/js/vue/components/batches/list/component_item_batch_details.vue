<template>
    <!-- <div>wda</div> -->

<v-layout wrap>
    <v-flex>
		<v-list subheader>
		    <v-subheader>
		    	<h2>HITs</h2>
		    </v-subheader>
		    <v-list-tile
		    	v-for="hit in props.item.hits"
		    >
		        <v-layout>
		            <v-flex shrink>
		                Valid CSV:  
		            </v-flex>
		            <v-flex>
		                    <v-icon color="success">check</v-icon>
		            </v-flex>
		        </v-layout>       
		    </v-list-tile>
		</v-list>
	</v-flex>
</v-layout>
    
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';

export default {
    name: 'component-item-batch',
    props: {
        props: {
            type: Object,
            required: true,
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