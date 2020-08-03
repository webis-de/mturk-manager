<template>
  <v-row no-gutters>
    <v-col>
      <v-row dense>
        <v-col class="shrink">
          {{ label }}
        </v-col>
        <v-spacer />
        <template v-if="showPreview === true">
          <slot></slot>
          <v-col class="shrink">
            <v-btn
              small
              icon
              v-on:click="isLayoutHorizontal = !isLayoutHorizontal"
            >
              <v-icon>mdi-table-{{ isLayoutHorizontal ? 'row' : 'column' }}</v-icon>
            </v-btn>
          </v-col>
        </template>
        <v-col class="shrink">
          <v-btn
            small
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
<!--          <v-overlay-->
<!--            v-if="isIframeLoaded === false"-->
<!--            absolute-->
<!--          >-->
<!--            <v-progress-circular indeterminate />-->
<!--          </v-overlay>-->

          <div class="iframe-container">
            <iframe
              style="background-color: white"
              v-bind:srcdoc="sourcePreview"
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
    sourcePreview: {
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
    };
  },
  computed: {
    sizes() {
      return {
        cols: this.showPreview === true && this.isLayoutHorizontal === true ? 6 : 12,
      };
    },
  },
  watch: {
    showPreview() {
      this.isIframeLoaded = false;
    },
    sourcePreview() {
      this.isIframeLoaded = false;
    },
  },
};
</script>

<style>
.CodeMirror {
  height: 60vh !important;
}
.iframe-container {
  overflow: hidden;
  padding-top: 60vh;
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
