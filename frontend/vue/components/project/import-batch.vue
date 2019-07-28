<template>
  <v-dialog
    v-model="dialog"
    max-width="1000"
    lazy
  >
    <v-btn
      slot="activator"
      color="primary"
      class="ml-0"
    >
      <v-icon left>
        cloud_upload
      </v-icon>
      Import CSV
    </v-btn>

    <v-card>
      <v-container
        fluid
        pa-0
      >
        <v-layout>
          <v-flex xs>
            <v-card-title>
              <span class="headline">Import from MTurk</span>
              <v-spacer />
              <v-btn
                icon
                v-on:click="dialog = false"
              >
                <v-icon>close</v-icon>
              </v-btn>
            </v-card-title>

            <v-card-text>
              <v-layout>
                <v-flex shrink>
                  <!--              {{ statistics }}-->
                  <upload-button
                    ref="upload-button"
                    class="px-0"
                    title="Select CSV"
                    v-on:file-update="fileChanged"
                  >
                    <template v-slot:icon-left>
                      <v-icon left>
                        attachment
                      </v-icon>
                    </template>
                  </upload-button>
                </v-flex>
                <!--                <v-flex>-->
                <!--                  <v-btn-->

                <!--                  >-->
                <!--                    <v-icon>cloud_upload</v-icon>-->
                <!--                    Upload-->
                <!--                  </v-btn>-->
                <!--                </v-flex>-->
              </v-layout>
            </v-card-text>

            <v-card-text v-if="info !== null">
              <v-layout
                v-bind:key="item.label"
                v-for="item in info"
              >
                <v-flex xs3>
                  {{ item.label }}
                </v-flex>
                <v-flex>
                  {{ item.value }}
                </v-flex>
              </v-layout>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <!--        <v-btn-->
              <!--          flat-->
              <!--          color="warning"-->
              <!--        >-->
              <!--          Clear-->
              <!--        </v-btn>-->
            </v-card-actions>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
import UploadButton from 'vuetify-upload-button';
import Papa from 'papaparse';
import {Service_Batches} from '../../services/service_batches';

export default {
  name: 'ImportBatch',
  components: {
    UploadButton,
  },
  data() {
    return {
      dialog: false,
      isParsingCSV: true,
      parsedCSV: null,
    };
  },
  computed: {
    info() {
      if (this.parsedCSV === null) return null;

      const info = [
        { label: 'Title', value: this.parsedCSV.data[0].Title },
        { label: 'Description', value: this.parsedCSV.data[0].Description },
        { label: 'HITs', value: Object.keys(this.parsedCSV.data.map(line => line.HITId).reduce((objectIds, idHIT) => ({ ...objectIds, [idHIT]: true }), {})).length },
        { label: 'Assignments', value: this.parsedCSV.data.length },
      ];

      return info;
    },
  },
  methods: {
    fileChanged(file) {
      if (file == null) {
        return;
      }

      this.isParsingCSV = true;
      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: (data) => {
          console.warn('results', data);
          this.parsedCSV = data;

          Service_Batches.findSettingsBatch(data.data[0]);
          // this.$store.commit('moduleBatches/setState', {
          //   objectState: results,
          //   nameState: 'objectCSVParsed',
          // });
        },
      });
    },
  },
};
</script>

<style scoped>

</style>
