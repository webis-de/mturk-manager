import humanizeDuration from 'humanize-duration';
import { VALIDATIONS, DESCRIPTIONS } from '../classes/enums';
import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
import Project from '../classes/project';
export default {
	data() {
		return {
			project: new Project(),
			valid: false,
            rules_title: [
                VALIDATIONS.REQUIRED,
            ],
            // description: '',
            rules_description: [
                VALIDATIONS.REQUIRED,
            ],
            // reward: 0,
            rules_reward: [
                VALIDATIONS.REQUIRED,
            ],
            // assignments_max: 1,
            rules_assignments_max: [
                VALIDATIONS.REQUIRED,
                VALIDATIONS.POSITIVE,
            ],
            // lifetime: 1,
            rules_lifetime: [
                VALIDATIONS.REQUIRED,
                VALIDATIONS.POSITIVE,
            ],
            // duration: 1,
            rules_duration: [
                VALIDATIONS.REQUIRED,
                VALIDATIONS.POSITIVE,
            ],
            // keywords: [],
            rules_keywords: [
            ],

            DESCRIPTIONS: DESCRIPTIONS,
		}
	},
	methods: {
    	format_duration(label, duration) {
    		return `${label} (${humanizeDuration(duration * 1000)})`;
    	},
        remove(item) {
            this.project.keywords.splice(this.project.keywords.indexOf(item), 1)
            this.project.keywords = [...this.project.keywords]
        },
	},
    created() {
        this.project.title = this.project_current.title;
        this.project.description = this.project_current.description;
        this.project.reward = this.project_current.reward;
        this.project.assignments_max = this.project_current.assignments_max;
        this.project.lifetime = this.project_current.lifetime;
        this.project.duration = this.project_current.duration;
    //     this.project.keywords = [
				// {
				// 	text: 'foo',
				// 	value: 1,
				// },];
        this.project.keywords = this.project_current.keywords;
    },
    computed: {
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
    },
}