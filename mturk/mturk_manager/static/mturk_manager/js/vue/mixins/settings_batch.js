import humanizeDuration from 'humanize-duration';
import { VALIDATIONS, DESCRIPTIONS } from '../classes/enums';
import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
export default {
	data() {
		return {
			valid: false,
            title: '',
            rules_title: [
                VALIDATIONS.REQUIRED,
            ],
            description: '',
            rules_description: [
                VALIDATIONS.REQUIRED,
            ],
            reward: 0,
            rules_reward: [
                VALIDATIONS.REQUIRED,
            ],
            assignments_max: 1,
            rules_assignments_max: [
                VALIDATIONS.REQUIRED,
                VALIDATIONS.POSITIVE,
            ],
            lifetime: 1,
            rules_lifetime: [
                VALIDATIONS.REQUIRED,
                VALIDATIONS.POSITIVE,
            ],
            duration: 1,
            rules_duration: [
                VALIDATIONS.REQUIRED,
                VALIDATIONS.POSITIVE,
            ],
            keywords: [],
            rules_keywords: [
            ],

            DESCRIPTIONS: DESCRIPTIONS,
		}
	},
	methods: {
    	format_duration(label, duration) {
    		return `${label} (${humanizeDuration(duration * 1000)})`;
    	},
	},
    created() {
    	console.log(this.project_current);
        this.title = this.project_current.title;
        this.description = this.project_current.description;
        this.reward = this.project_current.reward;
        this.assignments_max = this.project_current.assignments_max;
        this.lifetime = this.project_current.lifetime;
        this.duration = this.project_current.duration;
        this.keywords = this.project_current.keywords;
    },
    computed: {
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
    },
}