import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
export default {
	methods: {
		...mapActions('moduleProjects', {
			'set_slug_project_current': 'set_slug_project_current',
		}),
	},
    created() {
		const slug_project = this.$route.params.slug_project;
		if(slug_project != undefined)
		{
			this.set_slug_project_current(slug_project);
		}
    },
}