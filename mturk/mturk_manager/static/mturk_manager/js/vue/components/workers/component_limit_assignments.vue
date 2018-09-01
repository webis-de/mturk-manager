<template>
<td> 
		<!-- v-bind:return-value.sync="worker.count_assignments_limit" -->
	<v-edit-dialog
		v-if="project_current.count_assignments_max_per_worker > -1 && worker.count_assignments_limit != undefined"
		lazy
		persistent
		large
		v-on:save="save"
	>
		<div v-bind:class="{ 'warning--text' : has_reached_limit_assignments}">{{ content }}</div>
		<v-text-field
			type="number"
			slot="input"
			v-model="limit"
			label="Edit"
			single-line
			autofocus
            append-icon="clear"
            v-on:click:append="limit = 0"
		></v-text-field>
	</v-edit-dialog>

	<template
		v-else-if="project_current.count_assignments_max_per_worker > -1"
	>
	    <v-progress-circular
	      indeterminate
	      v-bind:width="2"
	      v-bind:size="24"
	    ></v-progress-circular>
	</template>

	<template
		v-else
	>No limit</template>

    <v-snackbar
        v-model="show_snackbar"
        v-bind:timeout="1000"
        color="info"
        bottom
    >
        Updated
        <v-btn
            flat
            v-on:click="show_snackbar = false"
        >
            Close
        </v-btn>
    </v-snackbar>  
</td>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
export default {
  	name: 'component-limit-assignments',
    props: {
        worker: {
            type: Object,
            required: true,
        }
    },
	data () {
		return {
			limit: this.worker.count_assignments_limit,
			show_snackbar: false,
		}
	},
	watch: {
		'worker.count_assignments_limit': function() {
			this.limit = this.worker.count_assignments_limit;
		},
	},
	computed: {
		content() {	
    		return `${this.worker.count_assignments_limit} of ${this.project_current.count_assignments_max_per_worker}`;
		},
        has_reached_limit_assignments() {
            return this.worker.count_assignments_limit >= this.project_current.count_assignments_max_per_worker;
        },
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
	},
	methods: {
		save() {
            this.set_show_progress_indicator(true);
            this.update_count_assignments_limit({
                worker: this.worker, 
                value: this.limit,
            }).then(() => {
                this.show_snackbar = true;
                this.set_show_progress_indicator(false);
            });
		},
        ...mapActions('moduleWorkers', {
            'update_count_assignments_limit': 'update_count_assignments_limit',
        }),
        ...mapActions(['set_show_progress_indicator']),
	},
}
</script>

<style lang="css" scoped>
</style>