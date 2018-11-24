<template>
    <v-dialog 
        v-model="dialog"
        max-width="80%"
    >
        <v-btn
            slot="activator" 
            icon
            small
            v-on:click="dialog = true"
        >
            <v-icon color="warning">edit</v-icon>
        </v-btn>
      	<v-card>
	        <v-card-title>
	            <span class="headline">Edit Worker Template</span>
	            <v-spacer></v-spacer>
	            <v-btn icon v-on:click="dialog = false">
	                <v-icon>close</v-icon>
	            </v-btn>
	        </v-card-title>
	        <v-card-text>
	      		<v-form ref="form" lazy-validation>
					<v-text-field
			            required
			            label="Name"
			  			v-bind:value="template_worker.name"
			            v-on:input="template_worker.name=$event; $v.template_worker.name.$touch()"
		        		v-bind:error-messages="validation_errors.template_worker.name"
			        ></v-text-field>
					<v-text-field
						type="number"
			            required
			  			v-bind:value="template_worker.height_frame"
			            v-on:input="template_worker.height_frame=try_number($event); $v.template_worker.height_frame.$touch()"
			            label="Height"
		        		v-bind:error-messages="validation_errors.template_worker.height_frame"
			        ></v-text-field>
					<v-text-field
			            required
			  			v-bind:value="template_worker.template"
			            v-on:input="template_worker.template=$event; $v.template_worker.template.$touch()"
			            label="Template"
		        		v-bind:error-messages="validation_errors.template_worker.template"
			        ></v-text-field>

			        <v-select
			  			v-bind:value="template_worker.template_assignment"
			            v-on:input="template_worker.template_assignment = $event; $v.template_worker.template_assignment.$touch()"
			            v-bind:items="list_templates_assignment"
			            label="Assignment Template"
			            item-text="name"
			            item-value="id"
			            v-bind:error-messages="validation_errors.template_worker.template_assignment"
                		clearable
			        ></v-select>

			        <v-select
			  			v-bind:value="template_worker.template_hit"
			            v-on:input="template_worker.template_hit = $event; $v.template_worker.template_hit.$touch()"
			            v-bind:items="list_templates_hit"
			            label="HIT Template"
			            item-text="name"
			            item-value="id"
			            v-bind:error-messages="validation_errors.template_worker.template_hit"
                		clearable
			        ></v-select>

			        <v-select
			  			v-bind:value="template_worker.template_global"
			            v-on:input="template_worker.template_global = $event; $v.template_worker.template_global.$touch()"
			            v-bind:items="list_templates_global"
			            label="Global Template"
			            item-text="name"
			            item-value="id"
			            v-bind:error-messages="validation_errors.template_worker.template_global"
                		clearable
			        ></v-select>
		    	</v-form>

			    <v-btn
			        class="ml-0"
			        color="primary"
			        v-on:click="update()"
					v-bind:disabled="$v.$invalid"
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
</template>
<script>
	import validations from '../../../mixins/validations';
	import helpers from '../../../mixins/helpers';
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
    import { required, minValue, maxValue } from 'vuelidate/lib/validators'
	import Template_Worker from '../../../classes/template_worker';
    import {Service_Templates_Worker} from "../../../services/service_templates_worker";
export default {
    mixins: [
        helpers,
        validations,
    ],
    props: {
        template_worker_current: {
        }
    },
    data() {
    	return {
            template_worker: new Template_Worker(this.template_worker_current),
			dialog: false,
    	}

    },
    methods: {
		update() {
            if(this.$refs.form.validate()) 
            {
                Service_Templates_Worker.edit({
					template_worker_current: this.template_worker_current,
					template_worker_new: this.template_worker,
					project: this.project_current,
				}).then(() => {
                    this.dialog = false;
    				this.$emit('edited');
    				this.reset();
                });
            }
			// console.log(this.project_current);
		},	
    	reset() {
            this.template_worker = new Template_Worker(this.template_worker_current),
    		this.$v.$reset();
			this.$v.$touch();
    	},
		...mapActions('moduleProjects', {
			'edit_template_worker': 'edit_template_worker',
		}),
    },
    computed: {
		list_templates_assignment() {
            return _.orderBy(this.project_current.templates_assignment, (template) => template.name);
		},
		list_templates_hit() {
            return _.orderBy(this.project_current.templates_hit, (template) => template.name);
		},
		list_templates_global() {
            return _.orderBy(this.project_current.templates_global, (template) => template.name);
		},
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
    },
    watch: {
    	dialog() {
    		this.reset();
    	},
    },
    validations: {
    	template_worker: {
	    	name: {
	    		required,
	    	},
	    	height_frame: {
	    		required,
	    		minValue: minValue(1),
	    	},
	    	template: {
	    		required,
	    	},
	    	template_assignment: {
	    	},
	    	template_hit: {
	    	},
	    	template_global: {
	    	},
    	},
    },
    created() {
		this.$v.$touch();
	},
    components: {
    },	
}
</script>