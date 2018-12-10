<template>
<div>
    <h2 class="headline">Sandbox</h2>
    <v-dialog 
        v-model="dialog"
        max-width="500"
    >
	    <v-btn 
            slot="activator" 
	        color="warning"
	    >
            <v-icon>delete</v-icon>
	    	Clear Sandbox
		</v-btn>

		<v-card>
            <!-- <v-card-title>
                <span class="headline">Add Profile</span>
                <v-spacer></v-spacer>
                <v-btn icon v-on:click="dialog = false">
                    <v-icon>close</v-icon>
                </v-btn>
            </v-card-title> -->
            <v-card-text>
                Do you really want to clear the sandbox? 
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    flat
                    color="warning"
                    v-on:click="clear"
                >Clear</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</div>
</template>

<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import {Service_Projects} from "../../../services/service_projects";
export default {
	name: 'component-clear-sandbox',
    data() {
        return {
        	dialog: false,
        }
    },
    methods: {
    	async clear() {
    	    await Service_Projects.clear_sandbox();
    		this.dialog = false;
    	},
    	...mapActions('moduleProjects', {
    		'clear_sandbox': 'clear_sandbox',
    	}),
    },
    computed: {

    },
    components: {

    },
}
</script>

<style scoped>
</style>