<template>
<v-layout wrap>
    <v-flex>
    	<v-btn class="mx-3" v-bind:disabled="!is_valid_csv" v-bind:loading="is_uploading_batch" large color="success" v-on:click="submit">Submit Batch</v-btn>
    </v-flex>
</v-layout>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import Project from '../../../classes/project';
export default {
	name: 'component-submit-batch',
    props: {
        project: {
            required: true,
            type: Project|undefined,
        },
    },
	data () {
		return {
			is_uploading_batch: false,
		}
	},
	computed: {
        ...mapGetters('moduleProjects', {
            // 'project_current': 'get_project_current',
        }),
        ...mapGetters('moduleBatches', {
            'object_csv_parsed': 'get_object_csv_parsed',
            'component_form': 'get_component_form',
            'is_valid_csv': 'is_valid_csv',
        }),
	},
	methods: {
		submit() {
			if(this.validate())
			{
				this.is_uploading_batch = true;
				console.log('adding batch')
				this.add_batch({
					settings: this.project,
					data_csv: this.object_csv_parsed.data,
				}).then(() => {
					this.is_uploading_batch = false;
					console.log('done')
	            });
			}
		},
		validate() {
			return this.component_form.validate();
		},
		...mapActions('moduleBatches', {
			'add_batch': 'add_batch',
		}),
	},
}
</script>

<style lang="css" scoped>
</style>