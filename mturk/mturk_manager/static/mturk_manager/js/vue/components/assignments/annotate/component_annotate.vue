<template>
<div>
		<!-- v-bind:action="`/view/${this.project_current.slug}`" -->
	<form 
	 	v-on:submit.prevent="submit"
	>
		<input type="hidden" name="list_ids[]" value="1">
		<input type="hidden" name="list_ids[]" value="3">
	    <v-btn 
	    	type="submit"
	        color="primary"
	        v-bind:disabled="assignments_selected.length == 0"
	    >
	    	Annotate {{ assignments_selected.length }} assignment(s)
		</v-btn>
	</form>
</div>
</template>

<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
export default {
	name: 'component_annotate',
    data() {
        return {
        }
    },
    methods: {
    	submit() {
	  		window.open(this.url, '_blank');
    	}
    },
    computed: {
    	url() {
    		let url = `/view/${this.project_current.slug}?list_ids=[`;
    		
    		url += _.join(_.map(this.assignments_selected, (assignment) => assignment.id), ',');

    		return url + ']';
    	},
        ...mapState('moduleAssignments', {
            'assignments_selected': 'assignments_selected',
        }),
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
    },
    components: {

    },
}
</script>

<style scoped>
</style>