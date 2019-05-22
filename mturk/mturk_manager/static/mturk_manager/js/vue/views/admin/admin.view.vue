<template>
  <v-container>
    <v-layout>
      <v-flex>
        <h1 class="headline">
          Admin
        </h1>
        <table-messages-reject
          v-bind:load-page="loadPage"
          name-state-pagination="paginationMessagesRejectAdmin"
          name-local-storage-pagination="pagination_messages_reject_admin"
          name-state-columns-selected="arrayColumnsSelectedAdmin"
        />
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import TableMessagesReject from '../../components/messages-reject/table-messages-reject';
import { ServiceMessages } from '../../services/Service_Messages_Reject';

export default {
  name: 'AppAdmin',
  components: {
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
