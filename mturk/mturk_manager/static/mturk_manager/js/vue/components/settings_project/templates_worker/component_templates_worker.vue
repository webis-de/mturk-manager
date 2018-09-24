<template>
<div>
	<h1>Worker Templates</h1>
    <component-list-templates-worker></component-list-templates-worker>
</div>
</template>

<script>
    import ComponentListTemplatesWorker from './component_list_templates_worker.vue';
	// import settings_batch from '../../../mixins/settings_batch';
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
export default {
    // mixins: [
    //     settings_batch,
    // ],
	name: 'component-templates-worker',
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
        ComponentListTemplatesWorker
    },
}
</script>

<style scoped>
</style>