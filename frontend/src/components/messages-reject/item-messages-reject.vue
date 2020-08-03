<template>
  <base-table-item
    v-bind:key="this.item.id"
    v-bind:item="this.item"
  >
    <base-table-cell
      v-slot="{ item }"
      name="message"
      class="text-xs-left pl-4"
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

      <delete-message-reject
        v-bind:message="item"
      />
    </base-table-cell>
  </base-table-item>
</template>

<script>
import BaseTableItem from '@/components/base-table-item';
import DeleteMessageReject from '@/modules/message/components/delete/delete-message-reject';
import BaseTableCell from '../base-table-cell';
import MessageMakeDefault from './message-make-default';

export default {
  name: 'ItemMessagesReject',
  components: {
    DeleteMessageReject, BaseTableItem, MessageMakeDefault, BaseTableCell,
  },
  props: {
    item: {
      type: Object,
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
    templateGlobal() { return this.item; },
    stylesCell() {
      if (this.isCondensed) {
        return {
          height: 'unset !important',
          paddingLeft: '5px !important',
          paddingRight: '5px !important',
        };
      }
      return {};
    },
  },
};
</script>
