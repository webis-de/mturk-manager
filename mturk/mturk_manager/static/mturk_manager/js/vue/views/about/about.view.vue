<template>
  <v-container>
    <v-layout
      fill-height
      column
      justify-center
    >
      <v-flex shrink>
        <v-layout justify-center>
          <v-flex class="text-xs-center">
            <h1 class="headline">About</h1>
            <about />
            <v-btn
              small
              color="secondary"
              v-bind:to="{ name: 'dashboard' }"
            >
              Back
            </v-btn>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import About from '../../components/about/about';

export default {
  name: 'ViewAbout',
  components: { About },
};
</script>
