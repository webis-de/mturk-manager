<template>
  <tr
    v-bind:key="message.id"
    class="text-no-wrap"
  >
    <base-table-cell
      v-slot="{ item }"
      name="message"
      class="text-xs-left"
      v-bind:item="message"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      {{ item.message }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="actions"
      class="text-xs-right"
      v-bind:item="message"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      <base-delete-message
        v-bind:item="item"
      />
    </base-table-cell>
  </tr>
</template>

<script>
import BaseTableCell from '../base-table-cell';
import BaseDeleteMessage from '../base-delete-message';

export default {
  name: 'ItemMessagesReject',
  components: { BaseDeleteMessage, BaseTableCell },
  props: {
    props: {
      required: true,
    },
    arrayColumnsSelected: {
      type: Array,
      required: true,
    },
    isCondensed: {
      required: true,
      type: Boolean,
    },
  },
  data() {
    return {
      message: this.props.item,
    };
  },
  computed: {
    columnsSelected() {
      return this.arrayColumnsSelected.reduce((accumulator, column) => {
        accumulator[column] = column;
        return accumulator;
      }, {});
    },
  },
};
</script>
