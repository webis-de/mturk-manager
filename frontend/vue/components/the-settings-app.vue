<template>
  <v-card>
    <v-list dense>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title
            style="cursor: pointer"
            v-on:click="isActiveModeLight = !isActiveModeLight"
          >
            Light Mode
          </v-list-item-title>
        </v-list-item-content>
        <v-list-item-action class="my-0">
          <v-switch
            v-model="isActiveModeLight"
            color="primary"
          />
        </v-list-item-action>
      </v-list-item>

      <v-divider />

      <v-list-item v-on:click="">
        <v-dialog v-model="isOpenUpdateCredentials" width="500">
          <template v-slot:activator="{ on }">
            <v-list-item-content>
              <v-list-item-title v-on="on">
                Update Credentials
              </v-list-item-title>
            </v-list-item-content>
          </template>

          <v-card>
            <v-card-title>
              Update Credentials
            </v-card-title>
            <v-card-text>
              <the-update-credentials
                class="text-center"
                v-on:updated-credentials="updatedCredentials"
              />
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-list-item>

      <v-list-item v-on:click="">
        <v-dialog max-width="1000">
          <template v-slot:activator="{ on }">
            <v-list-item-content>
              <v-list-item-title v-on="on">
                About
              </v-list-item-title>
            </v-list-item-content>

            <v-list-item-icon>
              <changelog-notification />
            </v-list-item-icon>
          </template>

          <v-card>
            <v-card-title>
              About
            </v-card-title>
            <v-card-text>
              <about />
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
import { Service_App } from '../services/service.app';
import TheUpdateCredentials from './the-update-credentials';
import About from './about/about';
import ChangelogNotification from './about/changelog-notification';

export default {
  name: 'TheSettingsApp',
  components: { ChangelogNotification, About, TheUpdateCredentials },
  data() {
    return {
      isActiveModeLight: this.$store.state.module_app.isActiveModeLight,
      isOpenUpdateCredentials: false,
    };
  },
  watch: {
    isActiveModeLight() {
      Service_App.setLightMode(this.isActiveModeLight);
    },
  },
  methods: {
    updatedCredentials() {
      this.$emit('updated-credentials');
      this.isOpenUpdateCredentials = false;
    },
  },
};
</script>

<style scoped>

</style>
