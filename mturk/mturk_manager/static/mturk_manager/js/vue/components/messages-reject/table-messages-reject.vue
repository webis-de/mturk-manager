<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <base-table
    name-vuex-module="moduleMessages"
    name-state-pagination="paginationMessagesReject"
    name-local-storage-pagination="pagination_messages_reject"

    v-bind:function-load-page="loadPage"
    v-bind:array-items="arrayItems"

    name-state-columns="arrayColumns"
    name-state-columns-selected="array_columns_selected"
    v-bind:is-condensed="true"
  >
    <template v-slot:default="{ props, array_columns_selected, isCondensed }">
      <item-messages-reject
        v-bind:props="props"
        v-bind:array-columns-selected="array_columns_selected"
        v-bind:is-condensed="isCondensed"
      />
    </template>

    <template v-slot:actions>
      <item-add-message/>
    </template>
  </base-table>
</template>

<script>
import BaseTable from '../base-table';
import { ServiceMessages } from '../../services/Service_Messages_Reject';
import { mapState } from 'vuex';
import ItemMessagesReject from './item-messages-reject';
import ItemAddMessage from './item-add-message';

export default {
  name: 'TableMessagesReject',
  components: {ItemAddMessage, ItemMessagesReject, BaseTable },
  data() {
    return {
      loadPage: ServiceMessages.loadPageReject,
    };
  },
  computed: {
    ...mapState('moduleMessages', {
      arrayItems: 'arrayItemsReject',
    }),
  },
};
</script>
