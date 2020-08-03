<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-expansion-panel>
    <v-expansion-panel-header>
      <v-row no-gutters>
        <v-col>
          {{ release.name }}
        </v-col>
        <v-col class="text-right">
          <base-display-datetime
            v-bind:datetime="release.created"
            v-bind:only-date="true"
          />
        </v-col>
      </v-row>
    </v-expansion-panel-header>

    <v-expansion-panel-content>
      <div
        v-if="release.body === null"
        class="text-center"
      >
        <v-progress-circular indeterminate />
      </div>
      <template v-else>
        <div
          class="text-left"
          v-html="bodyCompiled"
        ></div>
      </template>
    </v-expansion-panel-content>
  </v-expansion-panel>
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
