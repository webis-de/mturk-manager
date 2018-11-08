<template>
<div>
    <h2 class="headline">Administration</h2>
    <v-dialog 
        v-model="dialog"
        max-width="500"
    >
	    <v-btn 
            slot="activator" 
	        color="error"
	    >
            <v-icon>delete_forever</v-icon>
	    	Delete Project
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
                Do you really want to delete this project? 
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    flat
                    color="error"
                    v-on:click="confirm"
                >Delete</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</div>
</template>

<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
export default {
	name: 'component_delete_project',
    data() {
        return {
        	dialog: false,
        }
    },
    methods: {
    	async confirm() {
    		await this.delete_project(this.$router);
    	},
    	...mapActions('moduleProjects', {
    		'delete_project': 'delete_project',
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