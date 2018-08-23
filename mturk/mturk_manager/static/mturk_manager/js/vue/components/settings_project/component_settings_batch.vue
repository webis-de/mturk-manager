<template>
<div>
	<h1>Batch Settings</h1>
	<v-form v-model="valid" lazy-validation>
        <v-text-field
            required
            v-model="project.title"
            label="Title"
            v-bind:rules="rules_title"
            v-bind:hint="DESCRIPTIONS.TITLE_HIT"
        ></v-text-field>

        <v-text-field
            required
            v-model="project.description"
            label="Description"
            v-bind:rules="rules_description"
            v-bind:hint="DESCRIPTIONS.DESCRIPTION_HIT"
        ></v-text-field>

        <v-text-field
            required
            type="number"
            v-model="project.reward"
            step="0.01"
            label="Reward"
            v-bind:rules="rules_description"
            v-bind:hint="DESCRIPTIONS.REWARD_HIT"
            append-icon="attach_money"
        ></v-text-field>

        <v-text-field
            required
            type="number"
            v-model="project.assignments_max"
            label="Number of Assignments"
            v-bind:rules="rules_assignments_max"
            v-bind:hint="DESCRIPTIONS.ASSIGNEMENTS_MAX_HIT"
            min="1"
        ></v-text-field>

        <v-text-field
            required
            type="number"
            v-model="project.count_assignments_max_per_worker"
            label="Number of Maximal Assignments Per Worker"
            v-bind:rules="rules_count_assignments_max_per_worker"
            min="-1"
        ></v-text-field>
            <!-- v-bind:hint="DESCRIPTIONS.ASSIGNEMENTS_MAX_HIT" -->

        <v-text-field
            required
            type="number"
            v-model="project.lifetime"
            v-bind:label="format_duration('Lifetime', project.lifetime)"
            v-bind:rules="rules_lifetime"
            v-bind:hint="DESCRIPTIONS.LIFETIME_HIT"
            min="1"
            suffix="s"
        ></v-text-field>

        <v-text-field
            required
            type="number"
            v-model="project.duration"
            v-bind:label="format_duration('Duration', project.duration)"
            v-bind:rules="rules_duration"
            v-bind:hint="DESCRIPTIONS.DURATION_HIT"
            min="1"
            suffix="s"
        ></v-text-field>
    		<!-- v-bind:search-input.sync="search" -->

        <v-select
            v-model="project.template"
            v-bind:items="project.templates"
            label="Worker Template"
            item-text="name"
            item-value="id"
        ></v-select>

        <v-switch
            label="Soft Block Workers"
            v-model="project.block_workers"
        ></v-switch>
            
        <v-combobox
            v-model="project.keywords"
            v-bind:rules="rules_keywords"
            label="Keywords (Separated with TAB)"
            v-bind:hint="DESCRIPTIONS.KEYWORDS_HIT"
            v-bind:items="list_keywords"

    		hide-selected
            chips
            clearable
            multiple
            counter
            append-icon
        >
            <template slot="selection" slot-scope="data">
                <v-chip
                    v-bind:selected="data.selected"
                    close
                    @input="remove(data.item)"
                >
                    <strong>{{ data.item.text != undefined ? data.item.text : data.item }}</strong>&nbsp;
                </v-chip>
            </template>
        </v-combobox>
    </v-form>
        <!-- {{search}} -->
        {{project.keywords}}

    <v-btn
        color="primary"
        v-on:click="update()"
    >Update</v-btn>
</div>
</template>

<script>
	import settings_batch from '../../mixins/settings_batch';
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
export default {
    mixins: [
        settings_batch,
    ],
	name: 'component_settings_batch',
	data () {
		return {
			// search: undefined,
		}
	},
	methods: {
		update() {
			this.edit_project({
				project: this.project_current,
				project_new: this.project,
			}).then(() => {
				console.log('done')
            });
			// console.log(this.project_current);
		},	
		...mapActions('moduleProjects', {
			'edit_project': 'edit_project',
		}),
	},
    computed: {
    },
}
</script>

<style scoped>
</style>