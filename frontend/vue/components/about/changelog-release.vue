<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-expansion-panel-content lazy>
    <template
      v-slot:header=""
    >
      <v-layout>
        <v-flex>
          {{ release.name }}
        </v-flex>
        <v-flex class="text-xs-right">
          <base-display-datetime
            v-bind:datetime="release.created"
            v-bind:only-date="true"
          />
        </v-flex>
      </v-layout>
    </template>

    <v-card>
      <v-card-text>
        <div
          v-if="release.body === null"
          class="text-xs-center"
        >
          <v-progress-circular indeterminate />
        </div>
        <template v-else>
          <div v-html="bodyCompiled"></div>
        </template>
      </v-card-text>
    </v-card>
  </v-expansion-panel-content>
</template>


<script>
import marked from 'marked';
import BaseDisplayDatetime from '../common/base-display-datetime';

export default {
  name: 'ChangelogRelease',
  components: { BaseDisplayDatetime },
  props: {
    release: {
      required: true,
      type: Object,
    },
  },
  computed: {
    bodyCompiled() {
      return marked(this.release.body);
    },
  },
};
</script>
<style scoped>

</style>
