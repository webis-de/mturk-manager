<template>
  <v-tooltip top>
    <span slot="activator">
      {{ durationFormatted }}
    </span>
    {{ durationFormattedStrict }}s
  </v-tooltip>
</template>

<script>
// import helpers from '../mixins/helpers';
import { distanceInWords, isDate } from 'date-fns';

export default {
  // mixins: [
  //     // helpers,
  // ],
  name: 'BaseDisplayDuration',
  props: {
    start: {
      required: true,
      type: Date | undefined,
    },
    end: {
      required: true,
      type: Date | undefined,
    },
  },
  computed: {
    durationFormatted() {
      if (isDate(this.start) && isDate(this.end)) {
        return distanceInWords(this.start, this.end);
      }
      return '';
    },
    durationFormattedStrict() {
      if (isDate(this.start) && isDate(this.end)) {
        return (this.end - this.start) / 1000.0;
      }
      return '';
    },
  },
};
</script>
