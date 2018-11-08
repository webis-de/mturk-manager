<template>
    <v-dialog 
        v-model="dialog"
        max-width="500"
    >
        <v-btn
            slot="activator" 
            icon
            small
            v-on:click="dialog = true"
        >
            <v-icon color="error">delete</v-icon>
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
                Do you really want to delete the assignment template '{{ template_worker.name }}'? 
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    flat
                    color="error"
                    v-on:click="remove()"
                >Delete</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
export default {
    props: {
        template_worker: {
        }
    },
    data() {
        return {
            dialog: false,
        }
    },
    methods: {
        remove() {
            this.delete_template_worker({
                project: this.project_current,
                template_worker: this.template_worker,
                callback: () => {
                    this.$emit('deleted');
                    this.dialog = false;
                },
            }).then(() => {
            });
        },
        ...mapActions('moduleProjects', {
            'delete_template_worker': 'delete_template_worker',
        }),
    },
    computed: {
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
    },
    components: {

    },
}
</script>

<style scoped>
</style>