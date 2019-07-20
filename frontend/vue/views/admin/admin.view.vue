<template>
  <v-container
    grid-list-md
    fluid
  >
    <v-layout>
      <v-flex xs>
        <h1 class="headline">
          Admin
        </h1>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex xs>
        <v-card class="pa-2">
          <table-messages-reject
            v-bind:load-page="loadPage"
            name-state-pagination="paginationMessagesRejectAdmin"
            name-local-storage-pagination="pagination_messages_reject_admin"
            name-state-columns-selected="arrayColumnsSelectedAdmin"
          />
        </v-card>
      </v-flex>

      <v-flex xs>
        <v-card
          class="pa-2"
          height="100%"
        >
          <info-size />
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import TableMessagesReject from '../../components/messages-reject/table-messages-reject';
import { ServiceMessages } from '../../services/Service_Messages_Reject';
import InfoSize from './components/info-size';

export default {
  name: 'AppAdmin',
  components: {
    InfoSize,
    TableMessagesReject,
  },
  data() {
    return {
      loadPage: ServiceMessages.loadPageRejectAll,
    };
  },
  computed: {
  },
  methods: {
  },
};
</script>
