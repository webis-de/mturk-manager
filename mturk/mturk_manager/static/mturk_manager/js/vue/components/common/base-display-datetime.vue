<template>
  <v-tooltip top>
    <span slot="activator">
      {{ datetime_formatted }}
    </span>
    {{ datetime }}
  </v-tooltip>
</template>

<script>
import { format } from 'date-fns';

export default {
  name: 'BaseDisplayDatetime',
  props: {
    datetime: {
      required: true,
      type: Date | undefined,
    },
  },
  computed: {
    datetime_formatted() {
      if (this.datetime === undefined) {
        return undefined;
      }

      return format(this.datetime, 'MMM D, YYYY H:mm A');
    },
  },
};
</script>
