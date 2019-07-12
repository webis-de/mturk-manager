<template>
  <v-bottom-sheet
    v-model="open"
    persistent
    inset
    hide-overlay
  >
    <v-card style="height: 50px">
      <v-layout style="height: 100%" wrap align-content-center>
        <v-flex shrink class="mx-3">Creating Batch</v-flex>
        <v-flex>
          <v-progress-linear
            v-bind:value="50"
            class="my-0"
            height="20"
          />
        </v-flex>
      <v-flex xs1></v-flex>
      </v-layout>
    </v-card>
  </v-bottom-sheet>
</template>

<script>
export default {
  name: 'TheProgressBar',
    props: {
      open: {
          required: true,
      }
    },
  data() {
    return {
    };
  },
};
</script>

<style scoped>

</style>
