<template>
<div>
	<v-dialog v-model="dialog">
		<v-btn 
			slot="activator" 
			color="primary"
			small
		><v-icon>add</v-icon> Add Profile</v-btn>
      	<v-card>
      		{{settings_batch}}
	        <v-card-title>
	            <span class="headline">Add Profile</span>
	            <v-spacer></v-spacer>
	            <v-btn icon v-on:click="dialog = false">
	                <v-icon>close</v-icon>
	            </v-btn>
	        </v-card-title>
	        <v-card-text>
	      		<v-form ref="form" v-model="valid" lazy-validation>
					<v-text-field
			            required
			  			v-bind:value="settings_batch.name"
			            label="Name"
			            v-on:input="settings_batch.name=$event; $v.settings_batch.name.$touch()"
		        		v-bind:error-messages="validation_errors.settings_batch.name"
			        ></v-text-field>

			        <component-form-settings-batch
			        	v-bind.sync="settings_batch"
			        	v-bind:v="$v"
			        	v-bind:validation_errors="validation_errors"
			        ></component-form-settings-batch>
		    	</v-form>
			    <v-btn
			        class="ml-0"
			        color="primary"
			        v-on:click="create()"
					v-bind:disabled="$v.$invalid"
			    >Create</v-btn>
			</v-card-text>
    	</v-card>
</v-dialog>

	<v-snackbar
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
	</v-snackbar>
</div>
</template>
<script>
	import ComponentFormSettingsBatch from './component_form_settings_batch';
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
	import settings_batch from '../../../mixins/settings_batch';
	import validations from '../../../mixins/validations';
    import { required, minValue } from 'vuelidate/lib/validators'
export default {
    mixins: [
        settings_batch,
        validations,
    ],
    data() {
    	return {
			dialog: true,
            show_snackbar: false,

            valid: false,
            // foo: 'settings_batch',
    	}
    },
    methods: {
        update1() {
            console.log(this.project.count_assignments_max_per_worker )
            this.project.count_assignments_max_per_worker = 2
            console.log(this.project.count_assignments_max_per_worker )
        },
		create() {
            if(this.$refs.form.validate()) 
            {
    			this.create_settings_batch({
    				settings_batch: this.settings_batch,
    				project: this.project_current,
    			}).then(() => {
    				console.log('done')
                    // this.update_fields();
                    this.show_snackbar = true;
                });
            }
			// console.log(this.project_current);
		},	
    	reset() {
    		// this.name = undefined;
    		// this.height_frame = 800;
    		// this.template = undefined;
    		this.$v.$reset();
    	},
		...mapActions('moduleProjects', {
			'create_settings_batch': 'create_settings_batch',
		}),
    },
    computed: {
    },
    validations: {
    	settings_batch: {
    		name: {
    			required,
    		},
    		title: {
    			required,
    		},
			description: {
    			required,
			},
			reward: {
    			required,
			},
			count_assignments: {
    			required,
			},
			count_assignments_max_per_worker: {
			},
			lifetime: {
    			required,
			},
			duration: {
    			required,
			},
			template: {
    			required,
			},
			block_workers: {
    			required,
			},
			keywords: {
			},
			has_content_adult: {
			},
			qualification_assignments_approved: {
			},
			qualification_hits_approved: {
			},
			qualification_locale: {
			},
    	},
    },
    watch: {
    	dialog() {
    		this.reset();
    	},
    },
	components: {
		ComponentFormSettingsBatch,
	},
}
</script>