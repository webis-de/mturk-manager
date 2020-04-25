<template>
  <v-dialog
    v-model="dialog"
    max-width="1000"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        color="primary"
        class="ml-0"
        v-on="on"
      >
        <v-icon left>
          mdi-cloud-upload
        </v-icon>
        Import CSV
      </v-btn>
    </template>

    <v-card>
      <v-container
        fluid
        pa-0
      >
        <v-row>
          <v-col xs>
            <v-card-title>
              <span class="headline">Import from MTurk</span>
              <v-spacer />
              <v-btn
                icon
                v-on:click="dialog = false"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-card-title>

            <v-card-text>
              <v-row>
                <v-col shrink>
                  <!--              {{ statistics }}-->
                  <upload-button
                    ref="upload-button"
                    class="px-0"
                    title="Select CSV"
                    v-on:file-update="fileChanged"
                  >
                    <template v-slot:icon-left>
                      <v-icon left>
                        mdi-attachment
                      </v-icon>
                    </template>
                  </upload-button>
                </v-col>
                <!--                <v-flex>-->
                <!--                  <v-btn-->

                <!--                  >-->
                <!--                    <v-icon>cloud_upload</v-icon>-->
                <!--                    Upload-->
                <!--                  </v-btn>-->
                <!--                </v-flex>-->
              </v-row>
            </v-card-text>

            <v-card-text
              v-if="info !== null"
              class="px-4"
            >
              <v-row>
                <v-col xs6>
                  <v-text-field
                    v-model="nameBatch"
                    label="Batch Name"
                  />
                </v-col>
              </v-row>

              <v-row>
                <v-col xs6>
                  <v-select
                    v-model="templateWorker"
                    v-bind:items="$store.state.moduleTemplates.arrayItemsWorkerAll"
                    label="Worker Template"
                    item-text="name"
                    item-value="id"
                    dense
                  />
                </v-col>
              </v-row>

              <v-row v-if="countSettingsBatch === 0">
                <v-col xs6>
                  <v-text-field
                    v-model="nameSettingsBatch"
                    label="Batch Profile Name"
                  />
                </v-col>
              </v-row>

              <v-row
                v-for="item in info"
                v-bind:key="item.label"
              >
                <v-col xs3>
                  {{ item.label }}
                </v-col>
                <v-col>
                  {{ item.value }}
                </v-col>
              </v-row>
              <v-btn
                slot="activator"
                color="primary"
                class="ml-0"
                v-bind:loading="loading"
                v-bind:disabled="$v.$invalid"
                v-on:click="importBatches()"
              >
                <!--                <v-icon left>-->
                <!--                  cloud_upload-->
                <!--                </v-icon>-->
                Import Batch
              </v-btn>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <!--        <v-btn-->
              <!--          text-->
              <!--          color="warning"-->
              <!--        >-->
              <!--          Clear-->
              <!--        </v-btn>-->
            </v-card-actions>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
import UploadButton from 'vuetify-upload-button';
import Papa from 'papaparse';
import { required, requiredIf } from 'vuelidate/lib/validators';
import { Service_Batches } from '../../services/service_batches';
import { ServiceTemplates } from '../../services/service_templates';
import { ServiceSettingsBatch } from '../../services/service_settings_batch';

export default {
  name: 'ImportBatch',
  components: {
    UploadButton,
  },
  data() {
    return {
      dialog: false,
      isParsingCSV: false,
      parsedCSV: null,
      nameBatch: null,
      templateWorker: null,
      loading: false,
      countSettingsBatch: 0,
      nameSettingsBatch: null,
    };
  },
  computed: {
    info() {
      if (this.parsedCSV === null) return null;

      const info = [
        { label: 'Title', value: this.parsedCSV.data[0].Title },
        { label: 'Description', value: this.parsedCSV.data[0].Description },
        { label: 'HITs', value: Object.keys(this.parsedCSV.data.map((line) => line.HITId).reduce((objectIds, idHIT) => ({ ...objectIds, [idHIT]: true }), {})).length },
        { label: 'Assignments', value: this.parsedCSV.data.length },
      ];

      return info;
    },
  },
  watch: {
    dialog(value) {
      if (value === true) {
        this.isParsingCSV = false;
        this.parsedCSV = null;
        this.nameBatch = null;
        this.templateWorker = null;
        this.nameSettingsBatch = null;
        this.loading = false;
      } else {
        this.$refs['upload-button'].clear();
      }
    },
  },
  created() {
    // ServiceTemplates.loadPageWorker({
    //
    // }, {
    //   fields: ['id', 'name'],
    // }, 'arrayItemsWorkerAll').then((data) => {
    // });
  },
  methods: {
    importBatches() {
      this.loading = true;
      Service_Batches.importBatches({
        nameBatch: this.nameBatch,
        nameSettingsBatch: this.nameSettingsBatch,
        templateWorker: this.templateWorker,
        parsedCSVs: [this.parsedCSV.data],
      }).then(() => {
        ServiceSettingsBatch.loadPage(this.$store.state.moduleSettingsBatch.paginationGeneral, {});
        this.dialog = false;
      });
    },
    fileChanged(file) {
      if (file == null) {
        return;
      }

      this.isParsingCSV = true;
      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: async (data) => {
          if (data.data.length > 0) {
            this.countSettingsBatch = (await Service_Batches.findSettingsBatch(data.data)).items_total;

            this.parsedCSV = data;
            this.isParsingCSV = false;
            // this.$store.commit('moduleBatches/setState', {
            //   objectState: results,
            //   nameState: 'objectCSVParsed',
            // });
          }
        },
      });
    },
  },
  validations: {
    nameBatch: {
      required,
    },
    templateWorker: {
      required,
    },
    nameSettingsBatch: {
      required: requiredIf((component) => component.countSettingsBatch === 0),
    },
    parsedCSV: {
      required,
    },
  },
};
</script>

<style scoped>

</style>
