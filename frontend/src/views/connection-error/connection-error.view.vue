<template>
  <v-container class="fill-height">
    <v-row
      class="fill-height"
      justify="center"
    >
      <v-col>
        <v-row
          class="fill-height"
          align="center"
        >
          <v-col class="text-center">
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
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ComponentConnectionError',
};
</script>
