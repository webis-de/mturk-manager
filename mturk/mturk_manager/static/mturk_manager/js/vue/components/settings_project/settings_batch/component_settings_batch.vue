<template>
<div>
	<h2 class="headline">Batch Profiles</h2>
    <component-list-settings-batch></component-list-settings-batch>
</div>
</template>

<script>
    import ComponentListSettingsBatch from './component_list_settings_batch.vue';
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
export default {
	name: 'component_settings_batch',
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
        ComponentListSettingsBatch
    },
}
</script>

<style scoped>
</style>