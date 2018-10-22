<template>
<v-layout align-center>
	<v-flex xs6>
	    <v-progress-linear 
	    	class="my-0" 
	    	v-model="progress"
	    	v-bind:color="progress >= 100 ? 'success': 'primary'"
		></v-progress-linear>
	</v-flex>
	<v-flex class="px-2 text-no-wrap" shrink >
		<slot></slot>
	</v-flex>
</v-layout>
</span>
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
export default {
    name: 'component-progress',
    props: {
    	progress: {
    		required: true,
    		type: Number,
    	}
    },
    data () {
        return {
        }
    },
    computed: {
       
    },
    methods: {
    },
    components: {
    },
}
</script>