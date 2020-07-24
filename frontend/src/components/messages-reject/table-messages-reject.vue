<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <base-table
    title="Reject Messages"

    name-vuex-module="moduleMessages"
    v-bind:name-state-pagination="nameStatePagination"
    v-bind:name-local-storage-pagination="nameLocalStoragePagination"

    v-bind:array-items="arrayItems"

    name-state-columns="arrayColumns"
    v-bind:name-state-columns-selected="nameStateColumnsSelected"
    v-bind:is-condensed="true"

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
      <!--      <item-add-message-->
      <!--        v-on:create="refresh()"-->
      <!--      />-->
    </template>
  </base-table>
</template>

<script>
import { mapState } from 'vuex';
import CreateMessage from '@/modules/message/components/create-message';
import BaseTable from '../base-table';
import { ServiceMessages } from '../../services/messages-reject.service';
import ItemMessagesReject from './item-messages-reject';
import ItemAddMessage from './item-add-message';

export default {
  name: 'TableMessagesReject',
  components: {
    CreateMessage, ItemAddMessage, ItemMessagesReject, BaseTable,
  },
  props: {
    loadPage: {
      required: false,
      type: Function,
      default: ServiceMessages.loadPageReject,
    },
    nameStatePagination: {
      required: false,
      type: String,
      default: 'paginationMessagesReject',
    },
    nameLocalStoragePagination: {
      required: false,
      type: String,
      default: 'pagination_messages_reject',
    },
    nameStateColumnsSelected: {
      required: false,
      type: String,
      default: 'objectColumnsSelectedInitialGeneral',
    },
  },
  computed: {
    arrayItems() {
      const { arrayItemsReject } = this.$store.state.moduleMessages;

      return arrayItemsReject === null ? [] : arrayItemsReject;
    },
  },
};
</script>
