<template>
  <v-row no-gutters>
    <v-col>
      <v-row dense>
        <v-col class="shrink">
          {{ label }}
        </v-col>
        <v-spacer />
        <template v-if="showPreview === true">
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
          <v-col class="shrink">
            <v-btn
              x-small
              icon
              v-on:click="isLayoutHorizontal = !isLayoutHorizontal"
            >
              <v-icon>mdi-table-{{ isLayoutHorizontal ? 'row' : 'column' }}</v-icon>
            </v-btn>
          </v-col>
        </template>
        <v-col class="shrink">
          <v-btn
            x-small
            color="secondary"
            v-on:click="showPreview = !showPreview"
          >
            Preview
          </v-btn>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col v-bind="sizes">
          <codemirror
            v-bind:value="value"
            v-bind:options="options"
            v-on:input="$emit('input', $event)"
          />
        </v-col>
        <v-col
          v-if="showPreview === true"
          v-bind="sizes"
          style="position: relative"
        >
          <v-overlay
            v-if="isIframeLoaded === false"
            absolute
          >
            <v-progress-circular indeterminate />
          </v-overlay>

          <div class="iframe-container">
            <iframe
              style="background-color: white"
              v-bind:srcdoc="valueProcessed"
              v-on:load="isIframeLoaded = true"
            >
              test
            </iframe>
          </div>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import Papa from 'papaparse';
import { codemirror } from 'vue-codemirror';
import 'codemirror/mode/htmlembedded/htmlembedded';
import 'codemirror/lib/codemirror.css';

import 'codemirror/theme/monokai.css';

export default {
  name: 'BaseEditor',
  components: {
    codemirror,
  },
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
      options: {
        mode: 'text/html',
        theme: 'monokai',
        // lineNumbers: true,
        viewportMargin: Infinity,
      },
      showPreview: false,
      isIframeLoaded: false,
      isLayoutHorizontal: true,

      csvParsed: null,
      isParsingCSV: false,
      dialogFile: false,
    };
  },
  computed: {
    sizes() {
      return {
        cols: this.showPreview === true && this.isLayoutHorizontal === true ? 6 : 12,
      };
    },
    valueProcessed() {
      return this.processTemplate(this.value);
    },
  },
  watch: {
    showPreview() {
      this.isIframeLoaded = false;
    },
    value() {
      this.isIframeLoaded = false;
    },
  },
  methods: {
    escapeRegExp(string) {
      // from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions
      return string.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
    },
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
  },
};
</script>

<style>
.CodeMirror {
  height: 80vh !important;
}
.iframe-container {
  overflow: hidden;
  padding-top: 80vh;
  position: relative;
}

.iframe-container iframe {
   border: 0;
   height: 100%;
   left: 0;
   position: absolute;
   top: 0;
   width: 100%;
}
</style>
