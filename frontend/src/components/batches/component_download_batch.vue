<template>
  <div>
    <v-tooltip
      top
      v-bind:disabled="isValidSelection"
    >
      <template v-slot:activator="{ on }">
        <v-btn
          small
          v-bind:loading="isDownloadingCsv"
          v-bind:disabled="
            isDownloadingCsv ||
              countBatchesToDownload === 0 ||
              !isValidSelection
          "
          color="secondary"
          v-on:click="dialog = true"
          v-on="on"
        >
          Download {{ countBatchesToDownload }} Batch(es)
          <v-icon right>
            mdi-cloud-download
          </v-icon>
        </v-btn>
      </template>

      Selected batches have an incompatible structure
    </v-tooltip>
    <v-dialog
      v-model="dialog"
      max-width="80%"
    >
      <v-card>
        <v-card-title>
          Download Batch(es)
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col>
              Include the following values:
              <v-treeview
                v-model="headersSelected"
                v-bind:items="arrayHeaders"
                selectable
                dense
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn
                color="primary"
                v-on:click="download_csv"
              >
                Download {{ countBatchesToDownload }} Batch(es)
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';
import Papa from 'papaparse';
import { STATUS_EXTERNAL, STATUS_INTERNAL } from '../../classes/enums';
import { Service_Batches } from '../../services/service_batches';

export default {
  name: 'ComponentDownloadBatch',
  data() {
    return {
      dialog: false,
      isDownloadingCsv: false,
      isValidSelection: true,

      arrayHeaders: [],
      headersSelected: [],
    };
  },
  computed: {
    countBatchesToDownload() {
      return Object.keys(this.batchesSelected).length;
    },
    batchesSelected() {
      return this.$store.state.moduleBatches.object_batches_selected;
    },
  },
  watch: {
    dialog() {
      this.headersSelected = [0, 1, 2];
    },
    batchesSelected() {
      this.headersSelected = [0, 1, 2];

      if (this.countBatchesToDownload === 0) {
        this.isValidSelection = true;
        return;
      }

      this.isDownloadingCsv = true;
      Service_Batches.get_download_info({
        batches: Object.keys(this.batchesSelected),
      }).then((response) => {
        this.isValidSelection = response.data.is_valid;
        this.isDownloadingCsv = false;

        const array_children_builtin = [];
        _.forEach(response.data.set_builtin, (value) => {
          array_children_builtin.push({
            id: `${0}__${value}`,
            name: value,
          });
        });

        const array_children_parameters = [];
        _.forEach(response.data.set_parameters, (value, index) => {
          array_children_parameters.push({
            id: `${1}__${index}`,
            name: index,
          });
        });

        const array_children_answer = [];
        _.forEach(response.data.set_answer, (value) => {
          array_children_answer.push({
            id: `${1}__${value}`,
            name: value,
          });
        });

        const arrayHeaders = [];
        if (_.size(array_children_builtin) > 0) {
          arrayHeaders.push({
            id: 0,
            name: 'builtin',
            children: array_children_builtin,
          });
        }
        if (_.size(array_children_parameters) > 0) {
          arrayHeaders.push({
            id: 1,
            name: 'parameters',
            children: array_children_parameters,
          });
        }
        if (_.size(array_children_answer) > 0) {
          arrayHeaders.push({
            id: 2,
            name: 'answer',
            children: array_children_answer,
          });
        }

        this.headersSelected = [0, 1, 2];

        this.arrayHeaders = arrayHeaders;
      });
    },
  },
  methods: {
    download_csv() {
      this.isDownloadingCsv = true;

      const headersSelected = [];
      console.log('this.headersSelected', this.headersSelected);
      _.forEach(this.headersSelected, (value) => {
        if (_.isNumber(value)) return true;

        headersSelected.push(value.split('__')[1]);
      });

      Service_Batches.download({
        batches: Object.keys(this.batchesSelected),
        values: headersSelected,
      }).then(() => {
        this.headersSelected = [0, 1, 2];
        this.dialog = false;
        this.isDownloadingCsv = false;
      });
    },
    normalize_answer(answer_raw) {
      const answer = {};
      if (Array.isArray(answer_raw.QuestionFormAnswers.Answer)) {
        _.forEach(answer_raw.QuestionFormAnswers.Answer, (value) => {
          answer[value.QuestionIdentifier] = value.FreeText;
        });
      } else {
        answer[
          answer_raw.QuestionFormAnswers.Answer.QuestionIdentifier
        ] = answer_raw.QuestionFormAnswers.Answer.FreeText;
      }

      return answer;
    },
  },
};
</script>

<style scoped></style>
