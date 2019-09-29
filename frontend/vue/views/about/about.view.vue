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
            <h1 class="headline">
              About
            </h1>
            <about />
            <v-btn
              small
              color="secondary"
              v-bind:to="{ name: 'dashboard' }"
            >
              Back
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import About from '../../components/about/about';

export default {
  name: 'ViewAbout',
  components: { About },
};
</script>
