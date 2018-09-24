import { VALIDATIONS, DESCRIPTIONS } from '../classes/enums';
import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
import Settings_Batch from '../classes/settings_batch';
export default {
	data() {
		return {
			settings_batch: new Settings_Batch(),
            
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

            rules_template_worker: [
                VALIDATIONS.REQUIRED,
            ],

            DESCRIPTIONS: DESCRIPTIONS,
		}
	},
    watch: {
        // project: { 
        //     handler: function() {
        //         this.$emit('update:project', this.settings_batch);
        //     },
        //     deep: true,
        // },
    },
	methods: {
        update_fields() {
            // this.settings_batch.title="teeest"
            // this.settings_batch.title = this.settings_batch_current.title;
            // this.settings_batch.description = this.settings_batch_current.description;
            // this.settings_batch.reward = this.settings_batch_current.reward;
            // this.settings_batch.assignments_max = this.settings_batch_current.assignments_max;
            // this.settings_batch.count_assignments_max_per_worker = this.settings_batch_current.count_assignments_max_per_worker;
            // this.settings_batch.lifetime = this.settings_batch_current.lifetime;
            // this.settings_batch.duration = this.settings_batch_current.duration;
            // this.settings_batch.keywords = JSON.parse(JSON.stringify(this.settings_batch_current.keywords));
            // this.settings_batch.templates = this.settings_batch_current.templates;
            // this.settings_batch.template = this.settings_batch_current.template;
            // this.settings_batch.block_workers = this.settings_batch_current.block_workers;
            // this.settings_batch.has_content_adult = this.settings_batch_current.has_content_adult;


            // this.settings_batch.qualification_assignments_approved = this.settings_batch_current.qualification_assignments_approved;
            // this.settings_batch.qualification_hits_approved = this.settings_batch_current.qualification_hits_approved;
            // this.settings_batch.qualification_locale = JSON.parse(this.settings_batch_current.qualification_locale);
        },  
        ...mapActions('moduleKeywords', {
            'load_keywords': 'load_keywords',
        }),
	},
    created() {
        this.update_fields();
        // this.load_keywords();
    },
    computed: {
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
        ...mapGetters('moduleKeywords', {
            'object_keywords': 'get_object_keywords',
        }),
    },
}