<template>
	<v-progress-linear
		v-bind:style="{width}"
		height="20"
		class="my-0 mx-auto"
		v-model="progress"
		v-bind:color="progress >= 100 ? 'success': 'primary'"
	>
		<slot></slot>
	</v-progress-linear>

<!--<v-layout align-center>-->
	<!--<v-flex xs6>-->
	    <!--<v-progress-linear-->
	    	<!--class="my-0"-->
	    	<!--v-model="progress"-->
	    	<!--v-bind:color="progress >= 100 ? 'success': 'primary'"-->
		<!--&gt;</v-progress-linear>-->
	<!--</v-flex>-->
	<!--<v-flex xs6 class="px-2">-->
		<!--<slot></slot>-->
	<!--</v-flex>-->
<!--</v-layout>-->

<!--<div align-center>-->
	<!--<v-flex xs6>-->
	    <!--<v-progress-linear-->
	    	<!--class="my-0"-->
	    	<!--v-model="progress"-->
	    	<!--v-bind:color="progress >= 100 ? 'success': 'primary'"-->
		<!--&gt;</v-progress-linear>-->
	<!--</v-flex>-->
	<!--<v-flex xs6 class="px-2">-->
		<!--<slot></slot>-->

	<!--</v-flex>-->
<!--</div>-->
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
export default {
    name: 'component-batch-progress',
    props: {
    	progress: {
    		required: true,
    		type: Number,
    	},
		width: {
    	    required: false,
			type: String,
			default: '200px',
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

<style lang="scss" scoped>
.v-progress-linear {
	/*width: 200px;*/
}
</style>