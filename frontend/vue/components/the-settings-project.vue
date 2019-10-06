<template>
  <v-card>
    <v-list dense>
      <v-list-item>
        <v-list-item-action class="my-0">
          <v-switch color="primary" v-model="isActiveModeLight" />
        </v-list-item-action>
        <v-list-item-title>Light Mode</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
import { Service_App } from '../services/service.app';

export default {
  name: 'TheSettingsProject',
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
};
</script>

<style scoped>

</style>
