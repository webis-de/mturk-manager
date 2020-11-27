<template>
  <v-layout wrap>
    <v-flex>
      <v-btn
        class="mx-3"
        v-bind:disabled="!is_valid"
        v-bind:loading="is_uploading_batch"
        large
        color="success"
        v-on:click="submit"
      >
        Submit Batch
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';
import { ServiceBatches } from '../../../services/batches.service';
import { ServiceProjects } from '../../../services/projects.service';

export default {
  name: 'ComponentSubmitBatch',
  props: {
    settingsBatch: {
      required: true,
      type: SettingsBatch,
    },
    is_invalid_settings_batch: {
      required: true,
      type: Boolean,
    },
    name_batch: {
      required: true,
      type: String | undefined,
    },
    costs: {
      required: true,
      type: Number | undefined,
    },
    is_creating_batch: {},
  },
  data() {
    return {
      is_uploading_batch: false,
    };
  },
  computed: {
    isInBudget() {
      let isInBudget = true;

      if (this.project_current.amount_budget_max !== null) {
        const sumCosts = this.use_sandbox ? this.project_current.sum_costs_max_sandbox : this.project_current.sum_costs_max;
        isInBudget = this.project_current.amount_budget_max >= this.costs + sumCosts;
      }
      this.$emit('is_in_budget', isInBudget);
      return isInBudget;
    },
    is_valid() {
      return ServiceBatches.isValidCSV()
        && !this.is_invalid_settings_batch
        && this.isInBudget;
      // && required(this.name_batch);
    },
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
    ...mapState('module_app', ['use_sandbox']),
  },
  methods: {
    async submit() {
      this.is_uploading_batch = true;

      this.settingsBatch.qualification_locale = this.settingsBatch.qualificationLocale;
      this.settingsBatch.qualification_assignments_approved = this.settingsBatch.qualificationAssignmentsApproved;
      this.settingsBatch.qualification_hits_approved = this.settingsBatch.qualificationHitsApproved;
      this.settingsBatch.block_workers = this.settingsBatch.blockWorkers;
      this.settingsBatch.count_assignments = this.settingsBatch.countAssignments;
      this.settingsBatch.count_assignments_map_per_worker = this.settingsBatch.countAssignmentsMaxPerWorker;
      this.settingsBatch.has_content_adult = this.settingsBatch.hasContentAdult;
      this.settingsBatch.template = this.settingsBatch.templateWorker;

      await ServiceBatches.create({
        name: this.name_batch,
        settings_batch: this.settingsBatch,
        data_csv: this.$store.state.moduleBatches.objectCSVParsed.data,
      });

      this.is_uploading_batch = false;
      this.$emit('update:is_creating_batch', false);

      ServiceProjects.startPollTasks();

      // ServiceBatches.load_page({
      //   page: 1,
      //   rowsPerPage: 25,
      //   sortBy: 'datetime_creation',
      // });
    },
  },
};
</script>

<style lang="css" scoped></style>
