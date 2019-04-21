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
    if (this.changelog.length === 0 || this.changelog[0].name !== this.$store.state.module_app.version) {
      await Service_App.loadChangelog();
    }

    await this.checkLoad(this.changelog[0]);

    await this.$store.dispatch('module_app/setState', {
      objectState: this.changelog[0].tag,
      nameState: 'versionSeen',
      nameLocalStorage: 'version_seen',
    });
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
