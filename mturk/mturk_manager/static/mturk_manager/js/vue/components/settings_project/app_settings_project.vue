<template>
<div>
    <v-layout wrap>
    	<v-flex xs6>
			<component-settings-batch>
			</component-settings-batch>
    	</v-flex>
	</v-layout>
</div>
</template>

<script>
    import ComponentSettingsBatch from './component_settings_batch.vue';

export default {
  name: 'app_settings_project',

  data () {
    return {

    }
  },
  components: {
  	ComponentSettingsBatch,
  }
}
</script>

<style lang="css" scoped>
</style>