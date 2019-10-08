<template>
  <v-card>
    <v-list dense>
      <v-list-item>
        <v-list-item-action class="my-0">
          <v-switch
            v-model="isActiveModeLight"
            color="primary"
          />
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>Light Mode</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider />

      <v-list-item v-on:click="">
        <v-dialog width="500">
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
    </v-list>
  </v-card>
</template>

<script>
import { Service_App } from '../services/service.app';
import TheUpdateCredentials from './the-update-credentials';

export default {
  name: 'TheSettingsApp',
  components: { TheUpdateCredentials },
  data() {
    return {
      isActiveModeLight: this.$store.state.module_app.isActiveModeLight,
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
    },
  },
};
</script>

<style scoped>

</style>
