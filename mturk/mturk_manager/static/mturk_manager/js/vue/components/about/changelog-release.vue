<template>
  <v-expansion-panel-content lazy>
    <template
      v-slot:header=""
    >
      <div>{{ release.name }}</div>
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

export default {
  name: 'ChangelogRelease',
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
