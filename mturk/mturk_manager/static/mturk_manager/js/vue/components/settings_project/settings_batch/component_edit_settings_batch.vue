<template>
<div>
	<v-dialog v-model="dialog">
		<v-btn slot="activator" color="primary"><v-icon>add</v-icon> Add Profile</v-btn>
      	<v-card>
	        <v-card-title>
	            <span class="headline">Create Batch</span>
	            <v-spacer></v-spacer>
	            <v-btn icon v-on:click="dialog = false">
	                <v-icon>close</v-icon>
	            </v-btn>
	        </v-card-title>
	        <v-card-text>
	      		<v-form ref="form" v-model="valid" lazy-validation>
			        <h2>General Settings</h2>
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
			            append-icon="clear"
			            v-on:click:append="project.count_assignments_max_per_worker = -1"
			        ></v-text-field>
			            <!-- v-on:click:clear="project.count_assignments_max_per_worker = -1" -->

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
			            v-bind:label="`Limit Block and Project Block for Workers (${project.block_workers ? 'enabled': 'disabled'})`"
			            v-model="project.block_workers"
			        ></v-switch>
			        <v-combobox
			            v-model="project.keywords"
			            v-bind:rules="rules_keywords"
			            label="Keywords (Separated with TAB)"
			            v-bind:hint="DESCRIPTIONS.KEYWORDS_HIT"

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
			            
			        <v-divider class="my-3"></v-divider>
			        <h2>Qualifications</h2>
			        <v-switch
			            v-bind:label="`Contains Adult Content`"
			            v-model="project.has_content_adult"
			        ></v-switch>

			        <v-text-field
			            required
			            type="number"
			            v-model.number="project.qualification_assignments_approved"
			            step="1"
			            max="100"
			            min="0"
			            label="Approved Assignments"
			            append-icon="%"
			        ></v-text-field>

			        <v-text-field
			            required
			            type="number"
			            v-model.number="project.qualification_hits_approved"
			            step="1"
			            min="0"
			            label="Approved HITs"
			        ></v-text-field>

			        <v-combobox
			            v-model="project.qualification_locale"
			            label="Locale (Separated with TAB)"
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
			                    @input="remove_qualification_locale(data.item)"
			                >
			                    <strong>{{ data.item.text != undefined ? data.item.text : data.item }}</strong>&nbsp;
			                </v-chip>
			            </template>
			        </v-combobox>
		            <!-- v-bind:rules="rules_description" -->
		            <!-- v-bind:hint="DESCRIPTIONS.REWARD_HIT" -->
		    	</v-form>
	        <!-- {{search}} -->
	        <!-- {{project.keywords}} -->

			    <v-btn
			        class="ml-0"
			        color="primary"
			        v-on:click="update()"
			    >Update</v-btn>
			</v-card-text>
    	</v-card>
</v-dialog>

	<!-- <v-snackbar
	    v-model="show_snackbar"
	    v-bind:timeout="1500"
	    bottom
	    color="success"
	>
	    Saved!
	    <v-btn
	        flat
	        v-on:click="show_snackbar = false"
	    >
	        Close
	    </v-btn>
	</v-snackbar> -->
</div>
</template>
<script>
	import settings_batch from '../../../mixins/settings_batch';
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
export default {
    mixins: [
        settings_batch,
    ],
    data() {
    	return {
			dialog: false,
            show_snackbar: false,
    	}
    },
    methods: {
        update1() {
            console.log(this.project.count_assignments_max_per_worker )
            this.project.count_assignments_max_per_worker = 2
            console.log(this.project.count_assignments_max_per_worker )
        },
		update() {
            if(this.$refs.form.validate()) 
            {
    			this.edit_project({
    				project: this.project_current,
    				project_new: this.project,
    			}).then(() => {
    				console.log('done')
                    this.update_fields();
                    this.show_snackbar = true;
                });
            }
			// console.log(this.project_current);
		},	
		...mapActions('moduleProjects', {
			'edit_project': 'edit_project',
		}),
    }
}
</script>