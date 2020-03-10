<template>
  <v-layout>
    <v-flex>
      <v-layout>
        <v-flex>
          <v-file-input
            ref="upload-button"
            label="Upload CSV"
            v-bind:loading="isParsingCSV"
            clearable
            v-on:change="fileChanged"
          />
        </v-flex>
      </v-layout>

      <v-dialog
        v-model="isParsingCSV"
        hide-overlay
        persistent
        width="300"
      >
        <v-card
          color="primary"
          dark
        >
          <v-card-text>
            Parsing CSV...
            <v-progress-linear
              indeterminate
              color="white"
              class="mb-0"
            />
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-flex>
  </v-layout>
</template>

<script>
import Papa from 'papaparse';

export default {
  name: 'ComponentUploadCsv',
  props: {},
  data() {
    return {
      isParsingCSV: false,
    };
  },
  methods: {
    fileChanged(file) {
      console.warn('file', file);
      if (file === null || file === undefined) {
        this.reset(false);
        return;
      }

      this.isParsingCSV = true;
      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: (results) => {
          this.isParsingCSV = false;
          this.$store.commit('moduleBatches/setState', {
            objectState: results,
            nameState: 'objectCSVParsed',
          });
        },
      });
    },
    reset(clearInput = true) {
      this.isParsingCSV = false;
      this.$store.commit('moduleBatches/setState', {
        objectState: null,
        nameState: 'objectCSVParsed',
      });

      if (clearInput === true) {
        // this.$refs['upload-button'].clear();
      }
    },
  },
};
</script>

<style scoped>
</style>
