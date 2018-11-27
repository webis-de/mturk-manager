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
	            <span class="headline">Edit Global Template</span>
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
			  			v-bind:value="template_global.name"
			            v-on:input="template_global.name=$event; $v.template_global.name.$touch()"
		        		v-bind:error-messages="validation_errors.template_global.name"
			        ></v-text-field>
					<v-textarea
			            required
			            rows="20"
			  			v-bind:value="template_global.template"
			            v-on:input="template_global.template=$event; $v.template_global.template.$touch()"
			            label="Template"
		        		v-bind:error-messages="validation_errors.template_global.template"
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
	import Template_Global from '../../../classes/template_global';
    import {Service_Templates} from "../../../services/service_templates";
export default {
    mixins: [
        helpers,
        validations,
    ],
    props: {
        template_global_current: {
        }
    },
    data() {
    	return {
            template_global: new Template_Global(this.template_global_current),
			dialog: false,
    	}

    },
    methods: {
		update(close) {
            if(this.$refs.form.validate()) 
            {
                Service_Templates.edit({
					type_template: 'global',
					template_current: this.template_global_current,
					template_new: this.template_global,
					project: this.project_current,
				}).then(() => {
    				if(close === true)
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
            this.template_global = new Template_Global(this.template_global_current),
    		this.$v.$reset();
			this.$v.$touch();
    	},
		...mapActions('moduleProjects', {
			'edit_template_global': 'edit_template_global',
		}),
    },
    computed: {
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
    	template_global: {
	    	name: {
	    		required,
	    	},
	    	template: {
	    		required,
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