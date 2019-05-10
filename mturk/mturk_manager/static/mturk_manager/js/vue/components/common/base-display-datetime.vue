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
    onlyDate: {
      required: false,
      type: Boolean,
      default: false,
    },
  },
  computed: {
    datetime_formatted() {
      if (this.datetime === undefined) {
        return undefined;
      }

      return format(this.datetime, this.templateFormat);
    },
    templateFormat() {
      let templateFormat = 'MMM D, YYYY H:mm A';

      if (this.onlyDate === true) {
        templateFormat = 'MMM D, YYYY';
      }

      return templateFormat;
    },
  },
};
</script>
