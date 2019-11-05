<template>
  <v-tooltip top>
    <template v-slot:activator="{ on }">
      <span v-on="on">{{ datetime_formatted }}</span>
    </template>
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
      let templateFormat = 'MMM DD, YYYY H:mm A';

      if (this.onlyDate === true) {
        templateFormat = 'MMM DD, YYYY';
      }

      return templateFormat;
    },
  },
};
</script>
