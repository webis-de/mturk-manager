<template>
  <div>
    <v-dialog
      v-model="dialog"
      max-width="500"
    >
      <template v-slot:activator="{ on }">
        <v-btn
          class="ml-0"
          color="warning"
          v-on="on"
        >
          <v-icon left>
            mdi-delete
          </v-icon>
          Clear Sandbox
        </v-btn>
      </template>

      <v-card>
        <!-- <v-card-title>
                <span class="headline">Add Profile</span>
                <v-spacer></v-spacer>
                <v-btn icon v-on:click="dialog = false">
                    <v-icon>close</v-icon>
                </v-btn>
            </v-card-title> -->
        <v-card-text>
          Do you really want to clear the sandbox?
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn
            text
            color="warning"
            v-on:click="clear"
          >
            Clear
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import { ServiceProjects } from '../../../services/projects.service';

export default {
  name: 'ComponentClearSandbox',
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    async clear() {
      await ServiceProjects.clearSandbox();
      this.dialog = false;
    },
    ...mapActions('moduleProjects', {
      clear_sandbox: 'clear_sandbox',
    }),
  },
  computed: {},
  components: {},
};
</script>

<style scoped></style>
