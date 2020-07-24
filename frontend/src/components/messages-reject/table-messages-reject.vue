<template>
  <!--    v-bind:is-condensed="true"-->
  <base-table
    title="Reject Messages"

    v-bind:array-items="$store.getters['moduleMessages/messagesReject']"

    name-vuex-module="moduleMessages"
    name-state-pagination="paginationMessagesReject"
    name-local-storage-pagination="pagination_messages_reject"

    name-state-columns="arrayColumns"
    name-state-columns-selected="objectColumnsSelectedInitialGeneral"

    v-bind:show-select="false"
  >
    <template v-slot:default="{ item, objectColumnsSelected, isCondensed, refresh }">
      <item-messages-reject
        v-bind:item="item"
        v-bind:object-columns-selected="objectColumnsSelected"
        v-bind:is-condensed="isCondensed"

        v-on:delete="refresh()"
      />
    </template>

    <template v-slot:actions="{ refresh }">
      <create-message />
    </template>
  </base-table>
</template>

<script>
import CreateMessage from '@/modules/message/components/create/create-message';
import BaseTable from '../base-table';
import ItemMessagesReject from './item-messages-reject';
import ItemAddMessage from './item-add-message';

export default {
  name: 'TableMessagesReject',
  components: {
    CreateMessage,
    ItemAddMessage,
    ItemMessagesReject,
    BaseTable,
  },
};
</script>
