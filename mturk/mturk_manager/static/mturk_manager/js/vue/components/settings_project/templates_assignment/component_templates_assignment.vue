<template>
<div>
	<h2 class="headline">Assignment Templates</h2>
    <component-list-templates-assignment></component-list-templates-assignment>
</div>
</template>

<script>
    import ComponentListTemplatesAssignment from './component_list_templates_assignment.vue';
	// import settings_batch from '../../../mixins/settings_batch';
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
export default {
    // mixins: [
    //     settings_batch,
    // ],
	name: 'component-templates-assignment',
	data () {
		return {
			// search: undefined,
		}
	},
	methods: {
	},
    computed: {
    },
    components: {
        ComponentListTemplatesAssignment
    },
}
</script>

<style scoped>
</style>