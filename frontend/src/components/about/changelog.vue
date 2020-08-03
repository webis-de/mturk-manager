<template>
  <v-row no-gutters>
    <v-col cols="12">
      <v-expansion-panels
        v-model="panelsOpened"
        multiple
      >
        <changelog-release
          v-for="release in changelog"
          v-bind:key="release.tag"
          v-bind:release="release"
        />
      </v-expansion-panels>
    </v-col>

    <v-col
      class="text-right"
      cols="12"
    >
      <v-btn
        small
        text
        color="primary"
        v-on:click="reset"
      >
        Reset
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
import { AppService } from '../../services/app.service';
import ChangelogRelease from './changelog-release';
import { compareVersions } from '../../helpers';

export default {
  name: 'Changelog',
  components: { ChangelogRelease },
  data() {
    return {
      panelsOpened: [0],
    };
  },
  computed: {
    changelog() {
      return this.$store.state.module_app.changelog;
    },
  },
  watch: {
    panelsOpened(listNew, listOld) {
      listNew.forEach((index) => {
        if (listOld[index] !== true) {
          const release = this.changelog[index];
          this.checkLoad(release);
        }
      });
    },
  },
  async created() {
    this.init();
  },
  methods: {
    // Todo: fix bug when panel is open and "reset" is pressed
    async init() {
      // check if changelog is empty or not up to date
      if (this.changelog.length === 0
        || compareVersions(this.changelog[0].tag, this.$store.state.module_app.version) === -1) {
        await AppService.loadChangelog();
      }

      if (this.changelog.length > 0) {
        await this.checkLoad(this.changelog[0]);

        this.panelsOpened = [0];

        await this.$store.dispatch('module_app/setState', {
          objectState: this.changelog[0].tag,
          nameState: 'versionSeen',
          nameLocalStorage: 'version_seen',
        });
      }
    },
    async reset() {
      await AppService.resetChangelog();
      await this.init();
      this.panelsOpened = [0];
    },
    async checkLoad(release) {
      if (release.body === null) {
        await AppService.loadRelease(release.id);
      }
    },
  },
};
</script>

<style scoped>

</style>
