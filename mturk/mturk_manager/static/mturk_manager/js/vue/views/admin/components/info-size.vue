<template>
  <v-layout
    fill-height
    column
    justify-center
  >
    <v-flex v-if="infoSize !== undefined">
      <v-layout>
        <v-flex xs4></v-flex>
        <v-flex xs4>Real</v-flex>
        <v-flex xs4>Sandbox</v-flex>
      </v-layout>
      <v-layout>
        <v-flex xs4>Batches</v-flex>
        <v-flex xs4>{{ infoSize[0] }}</v-flex>
        <v-flex xs4>{{ infoSize[1] }}</v-flex>
      </v-layout>
      <v-layout>
        <v-flex xs4>HITs</v-flex>
        <v-flex xs4>{{ infoSize[2] }}</v-flex>
        <v-flex xs4>{{ infoSize[3] }}</v-flex>
      </v-layout>
      <v-layout>
        <v-flex xs4>Assignments</v-flex>
        <v-flex xs4>{{ infoSize[4] }}</v-flex>
        <v-flex xs4>{{ infoSize[5] }}</v-flex>
      </v-layout>
    </v-flex>

    <v-flex
      v-else
      shrink
    >
      <v-layout justify-center>
        <v-progress-circular
          indeterminate
        />
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import { ServiceAdmin } from '../../../services/admin.service';

export default {
  name: 'InfoSize',
  data() {
    return {
      infoSize: undefined,
    };
  },
  created() {
    ServiceAdmin.loadInfoSize().then((result) => {
      this.infoSize = result;
    });
  },
};
</script>
