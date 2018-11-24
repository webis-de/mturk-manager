<template>
    <v-dialog 
        v-model="dialog"
        max-width="80%"
        persistent
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
	            <span class="headline">Edit HIT Template</span>
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
			  			v-bind:value="template_hit.name"
			            v-on:input="template_hit.name=$event; $v.template_hit.name.$touch()"
		        		v-bind:error-messages="validation_errors.template_hit.name"
			        ></v-text-field>
					<v-textarea
			            required
			            rows="20"
			  			v-bind:value="template_hit.template"
			            v-on:input="template_hit.template=$event; $v.template_hit.template.$touch()"
			            label="Template"
		        		v-bind:error-messages="validation_errors.template_hit.template"
			        ></v-textarea>
		    	</v-form>
			</v-card-text>

       	 	<v-card-actions>
			    <v-btn
			    	flat
			        class="ml-0"
			        color="înfo"
			        v-on:click="dialog = false; reset();"
					v-bind:disabled="$v.$invalid"
			    >Cancel</v-btn>
			    <v-spacer></v-spacer>
			    <v-btn
			    	flat
			        class="ml-0"
			        color="primary"
			        v-on:click="update()"
					v-bind:disabled="$v.$invalid"
			    >Save</v-btn>

			    <v-btn
			    	flat
			        class="ml-0"
			        color="success"
			        v-on:click="update(true)"
					v-bind:disabled="$v.$invalid"
			    >Save and Close</v-btn>
			</v-card-actions>
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
	import Template_HIT from '../../../classes/template_hit';
    import {Service_Templates_HIT} from "../../../services/service_templates_hit";
export default {
    mixins: [
        helpers,
        validations,
    ],
    props: {
        template_hit_current: {
        }
    },
    data() {
    	return {
            template_hit: new Template_HIT(this.template_hit_current),
			dialog: false,
    	}

    },
    methods: {
		update(close) {
            if(this.$refs.form.validate()) 
            {
                Service_Templates_HIT.edit({
					template_hit_current: this.template_hit_current,
					template_hit_new: this.template_hit,
					project: this.project_current,
				}).then(() => {
    				if(close == true)
    				{
                    	this.dialog = false;
    					this.reset();
    				}
    				this.$emit('edited');
                });
            }
			// console.log(this.project_current);
		},	
    	reset() {
            this.template_hit = new Template_HIT(this.template_hit_current),
    		this.$v.$reset();
			this.$v.$touch();
    	},
		...mapActions('moduleProjects', {
			'edit_template_hit': 'edit_template_hit',
		}),
    },
    computed: {
		list_templates_hit() {
            return _.orderBy(this.project_current.templates_hit, (template) => template.name);
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
    	template_hit: {
	    	name: {
	    		required,
	    	},
	    	template: {
	    		required,
    			contains_injection_assignments: (value) => value != undefined && value.indexOf(' data-inject_assignments') >= 0
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