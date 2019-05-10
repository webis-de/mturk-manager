<template>
  <v-expansion-panel
    v-model="panelsOpened"
    expand
  >
    <changelog-release
      v-for="release in changelog"
      v-bind:key="release.tag"
      v-bind:release="release"
    />
  </v-expansion-panel>
</template>

<script>
import { Service_App } from '../../services/service.app';
import ChangelogRelease from './changelog-release';
import { compareVersions } from '../../helpers';

export default {
  name: 'Changelog',
  components: { ChangelogRelease },
  data() {
    return {
      panelsOpened: [true],
    };
  },
  computed: {
    changelog() {
      return this.$store.state.module_app.changelog;
    },
  },
  watch: {
    panelsOpened(listNew, listOld) {
      // console.warn('listOld', JSON.stringify(listOld));
      // console.warn('listNew', JSON.stringify(listNew));

      listNew.forEach((isOpened, index) => {
        if (isOpened === true) {
          if (listOld[index] !== true) {
            const release = this.changelog[index];
            this.checkLoad(release);
          }
        }
      });
    },
  },
  async created() {
    // check if changelog is empty or not up to date
    if (this.changelog.length === 0
      || compareVersions(this.changelog[0].tag, this.$store.state.module_app.version) === -1) {
      await Service_App.loadChangelog();
    }

    if (this.changelog.length > 0) {
      await this.checkLoad(this.changelog[0]);

      await this.$store.dispatch('module_app/setState', {
        objectState: this.changelog[0].tag,
        nameState: 'versionSeen',
        nameLocalStorage: 'version_seen',
      });
    }
  },
  methods: {
    async checkLoad(release) {
      if (release.body === null) {
        await Service_App.loadRelease(release.id);
      }
    },
  },
};
</script>

<style scoped>

</style>
