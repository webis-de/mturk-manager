<template>
  <v-container class="fill-height">
    <v-row
      class="fill-height"
      justify="center"
    >
      <v-col cols="4">
        <v-row
          class="fill-height"
          align="center"
        >
          <v-col
            class="text-center"
          >
            <the-update-credentials />
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-snackbar
      v-bind:value="false"
      v-bind:timeout="0"
      color="error"
      top
    >
      Cannot connect to the database! Please check the credentials
    </v-snackbar>
  </v-container>
</template>

<script>

import TheUpdateCredentials from '../../components/the-update-credentials';
export default {
  name: 'AddCredentials',
  components: {TheUpdateCredentials},
};
</script>

<style scoped></style>
