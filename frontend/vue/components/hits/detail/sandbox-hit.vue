<template>
  <v-row dense>
    <v-col class="shrink">
      <v-dialog
        v-model="dialog"
        fullscreen
      >
        <template v-slot:activator="{ on }">
          <v-btn
            color="primary"
            small
            class="ml-0"
            v-on="on"
          >
            Show
          </v-btn>
        </template>

        <v-card>
          <v-toolbar
            dense
          >
            <v-spacer />
            <v-btn
              icon
              dark
              v-on:click="dialog = false"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-toolbar>
          <iframe
            ref="iframe"
            style="border-width: 0"
          ></iframe>
        </v-card>
      </v-dialog>
    </v-col>
    <v-col class="shrink">
      <v-btn
        color="primary"
        small
        class="ml-0"
        v-on:click="openSandbox"
      >
        View in new tab
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
import {
  mapGetters,
} from 'vuex';
import HIT from '../../../classes/hit';
import { getHeight, getWidth } from '../../../helpers';

export default {
  name: 'SandboxTemplate',
  props: {
    hit: {
      required: true,
      type: HIT,
    },
  },
  data() {
    return {
      dialog: false,
    };
  },
  computed: {
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  watch: {
    dialog() {
      if (this.dialog === true) {
        this.$nextTick(() => {
          this.$refs.iframe.width = getWidth();
          this.$refs.iframe.height = getHeight();

          let { template } = this.hit.batch.settings_batch.template;

          for (const entry of Object.entries(JSON.parse(this.hit.parameters))) {
            template = template.replace(`\${${entry[0]}}`, entry[1]);
          }

          this.$refs.iframe.srcdoc = template;
        });
      }
    },
  },
  methods: {
    openSandbox() {
      const url = `/sandbox/hit?slug_project=${this.project_current.slug}&id_hit=${this.hit.id}`;
      window.open(url, '_blank');
    },
  },
};
</script>

<style scoped>
  .v-card {
    background-color: white;
  }
</style>
