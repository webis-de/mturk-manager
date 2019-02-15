<template>
  <!-- <v-dialog v-model="show_dialog_policy" max-width="800px" persistent>
        <v-btn slot="activator" v-on:click="policy_to_be_edited = null" color="primary" dark class="mb-2">New Policy</v-btn>
        <v-card>
            <v-card-title>
              <span class="headline">{{ title_dialog_policy }}</span>
            </v-card-title>
            <v-card-text>
              <v-container grid-list-md>
                <v-layout wrap>
                  <v-flex xs12>
                    <v-text-field v-model="policy_dialog.name" label="Name"></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field v-model="policy_dialog.description" label="Description"></v-text-field>
                  </v-flex>
                  <v-flex xs12 sm6 md4>
                    <v-text-field v-model="policy_dialog.is_requestable" label="Is Requestable"></v-text-field>
                  </v-flex>
                  <v-flex xs12 sm6 md4>
                    <v-text-field v-model="policy_dialog.status" label="Status"></v-text-field>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" flat v-on:click.native="cancel">Cancel</v-btn>
              <v-btn color="blue darken-1" flat v-on:click.native="add_or_edit_policy">Save</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog> -->
</template>

<script>
// import { mapState, mapActions, mapGetters } from 'vuex';
// import { Policy } from '../../store/modules/policies.js';

// import ComponentShowBalance from './component-show-balance.vue';
// import ComponentShowMoneySpent from './component-show-money-spent.vue';
// import ComponentShowBatches from './component-show-batches.vue';
export default {
  name: 'component-add-qualification',
  props: {
    show_dialog_qualification_add: {
      required: true,
      type: Boolean,
    },
  },
  data() {
    return {};
  },
  computed: {},
  methods: {
    init() {
      console.log('init');
      setTimeout(() => {
        this.$emit('finished');
      }, 1000);
    },
  },
  watch: {
    show_dialog_qualification_add(value_new) {
      if (value_new == true) {
        this.init();
      } else {
        console.log('called but is false');
      }
    },
  },
};
</script>
