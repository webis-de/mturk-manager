<template>
  <base-editor
    v-bind:value="value"
    v-bind:source-preview="valueProcessed"
    v-bind:label="label"
    v-on:input="$emit('input', $event)"
  >
    <v-col class="shrink">
      <v-dialog
        v-model="dialogFile"
        max-width="500"
      >
        <template v-slot:activator="{ on }">
          <v-btn
            x-small
            icon
            v-on="on"
          >
            <v-icon>mdi-cloud-upload</v-icon>
          </v-btn>
        </template>
        <v-card>
          <v-card-title>Upload CSV</v-card-title>
          <v-card-text>
            <v-file-input
              label="CSV"
              accept=".csv"
              v-bind:loading="isParsingCSV"
              v-on:change="uploadedFile"
            />
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-col>
  </base-editor>
</template>

<script>
import Papa from 'papaparse';
import BaseEditor from '../../../app/components/base-editor';

export default {
  name: 'TemplateWorkerSandbox',
  components: { BaseEditor },
  props: {
    value: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: '',
    },
  },
  data() {
    return {
      csvParsed: null,
      isParsingCSV: false,

      dialogFile: false,
    };
  },
  computed: {

    valueProcessed() {
      return this.processTemplate(this.value);
    },
  },
  methods: {
    processTemplate() {
      if (this.csvParsed === null) {
        return this.value;
      }

      let result = this.value;
      for (const [key, value] of Object.entries(this.csvParsed)) {
        const re = new RegExp(this.escapeRegExp(`\${${key}}`), 'g');
        result = result.replace(re, value);
      }

      return result;
    },

    uploadedFile(file) {
      if (file === undefined) {
        this.isParsingCSV = false;
        this.csvParsed = null;
        return;
      }

      this.isParsingCSV = true;
      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        preview: 1,
        complete: (results) => {
          this.isParsingCSV = false;
          if (results.data.length > 0) {
            this.csvParsed = results.data[0];
          }
          this.dialogFile = false;
        },
      });
    },
    escapeRegExp(string) {
      // from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions
      return string.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
    },
  },
};
</script>

<style scoped>

</style>
