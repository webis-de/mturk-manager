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
            rules_count_assignments_max_per_worker: [
                VALIDATIONS.REQUIRED,
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
            
			list_keywords: [
			],
		}
	},
    watch: {
        project: { 
            handler: function() {
                this.$emit('update:project', this.project);
            },
            deep: true,
        },
    },
	methods: {
    	format_duration(label, duration) {
    		return `${label} (${humanizeDuration(duration * 1000)})`;
    	},
        remove(item) {
            this.project.keywords.splice(this.project.keywords.indexOf(item), 1)
            this.project.keywords = [...this.project.keywords]
        },
        update_fields() {
            this.project.title = this.project_current.title;
            this.project.description = this.project_current.description;
            this.project.reward = this.project_current.reward;
            this.project.assignments_max = this.project_current.assignments_max;
            this.project.count_assignments_max_per_worker = this.project_current.count_assignments_max_per_worker;
            this.project.lifetime = this.project_current.lifetime;
            this.project.duration = this.project_current.duration;
        //     this.project.keywords = [
                    // {
                    //  text: 'foo',
                    //  value: 1,
                    // },];
            this.project.keywords = JSON.parse(JSON.stringify(this.project_current.keywords));
            this.project.templates = this.project_current.templates;
            this.project.template = this.project_current.template;
            this.project.block_workers = this.project_current.block_workers;
        },
	},
    created() {
        this.update_fields();
    },
    computed: {
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
    },
}