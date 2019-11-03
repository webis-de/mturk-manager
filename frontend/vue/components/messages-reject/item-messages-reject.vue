<template>
  <tr
    v-bind:key="this.item.id"
    class="text-no-wrap"
  >
    <base-table-cell
      v-slot="{ item }"
      name="message"
      class="text-xs-left"
      v-bind:item="this.item"
      v-bind:columns-selected="objectColumnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      {{ item.message }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="count_usage"
      class="text-xs-right"
      v-bind:item="this.item"
      v-bind:columns-selected="objectColumnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      {{ item.count_usage }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="actions"
      class="text-xs-right"
      v-bind:item="this.item"
      v-bind:columns-selected="objectColumnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      <message-make-default
        v-bind:item="item"
      />

      <base-delete-message
        v-bind:item="item"

        v-on:delete="$emit('delete')"
      />
    </base-table-cell>
  </tr>
</template>

<script>
import BaseTableCell from '../base-table-cell';
import BaseDeleteMessage from '../base-delete-message';
import MessageMakeDefault from './message-make-default';

export default {
  name: 'ItemMessagesReject',
  components: { MessageMakeDefault, BaseDeleteMessage, BaseTableCell },
  props: {
    item: {
      required: true,
    },
    objectColumnsSelected: {
      type: Object,
      required: true,
    },
    isCondensed: {
      required: true,
      type: Boolean,
    },
  },
  computed: {
  },
};
</script>
