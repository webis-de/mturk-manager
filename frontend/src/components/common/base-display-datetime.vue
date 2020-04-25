<template>
  <v-tooltip top v-bind:open-delay="1000">
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
      let templateFormat = 'YYYY-MM-DD HH:mm';

      if (this.onlyDate === true) {
        templateFormat = 'YYYY-MM-DD';
      }

      return templateFormat;
    },
  },
};
</script>
