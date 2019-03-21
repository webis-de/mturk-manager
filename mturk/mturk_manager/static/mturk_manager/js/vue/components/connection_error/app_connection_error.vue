<template>
  <v-container>
    <v-layout wrap>
      <v-flex class="text-xs-center">
        <h3 class="display-1">
          Connection Error
        </h3>
        <p>
          No connection to the database could be established!
        </p>
        <v-btn
          color="primary"
          to="add_credentials"
        >
          Update credentials
        </v-btn>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'ComponentConnectionError',
};
</script>
