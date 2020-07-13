import {
  mapGetters,
} from 'vuex';
import { required, minValue, maxValue } from 'vuelidate/lib/validators';
import _ from 'lodash';
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';
import { DESCRIPTIONS } from '../classes/enums';
import { ServiceKeywords } from '../services/keywords.service';

const foo = (object_settings_batch, settingsBatch) => (value) => {
  if (_.get(settingsBatch, 'name', undefined) == value) return true;

  return (
    _.find(object_settings_batch, (settings_batch) => settings_batch.name == value) == undefined
  );
};

export const settingsBatch = {
  data() {
    return {
      settings_batch: new SettingsBatch(),
      DESCRIPTIONS,
    };
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
      if (this.settingsBatch !== undefined) {
        this.settings_batch = _.cloneDeep(this.settingsBatch);
      } else {
        this.settings_batch = new SettingsBatch();
      }
    },
  },
  created() {
    this.update_fields();
    ServiceKeywords.load();
  },
  computed: {
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  validations() {
    const validations = {
      settings_batch: {
        name: {
          required,
          is_unique: foo(
            this.project_current.settings_batch,
            this.settingsBatch,
          ),
        },
        title: {
          required,
        },
        description: {
          required,
        },
        reward: {
          required,
          minValue: minValue(0),
        },
        countAssignments: {
          required,
          minValue: minValue(0),
        },
        countAssignmentsMaxPerWorker: {
          minValue: minValue(0),
        },
        lifetime: {
          required,
          minValue: minValue(0),
        },
        duration: {
          required,
          minValue: minValue(30),
          maxValue: maxValue(31536000),
        },
        templateWorker: {
          required,
        },
        blockWorkers: {
          required,
        },
        keywords: {},
        hasContentAdult: {},
        qualificationAssignmentsApproved: {
          minValue: minValue(0),
          maxValue: maxValue(100),
        },
        qualificationHitsitsApproved: {
          minValue: minValue(0),
        },
        qualificationLocale: {},
      },
    };

    if (this.name_not_required) {
      delete validations.settings_batch.name.required;
    }

    return validations;
  },
};
