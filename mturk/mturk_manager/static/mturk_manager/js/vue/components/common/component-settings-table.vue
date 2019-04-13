<template>
  <div>
    <v-btn color="primary" v-on:click="dialog = true" small>
      Toggle Columns
    </v-btn>

    <v-dialog v-model="dialog" max-width="80%">
      <v-card>
        <v-card-text>
          <v-layout>
            <v-flex>
              <v-checkbox
                class="ma-0"
                label="Toggle all"
                v-model="isToggledAll"
                v-bind:indeterminate="is_indeterminate"
                hide-details
              ></v-checkbox>
            </v-flex>
          </v-layout>
          <v-layout>
            <v-flex>
              <v-checkbox
                class="ma-0"
                v-for="column in columns"
                v-bind:key="column.value"
                v-bind:label="column.label || column.text"
                v-bind:value="column.value"
                v-model="columnsSelectedIntern"
                hide-details
              ></v-checkbox>
            </v-flex>
          </v-layout>
          <v-layout row class="mt-3">
            <v-flex>
              <v-btn
                color="primary"
                v-on:click="
                  columnsSelectedIntern = columnsSelectedInitial;
                  dialog = false;
                "
                >Reset to default</v-btn
              >
              <v-btn flat v-on:click="dialog = false">Cancel</v-btn>
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import _ from 'lodash';

export default {
  name: 'ComponentSettingsTable',
  props: {
    columns: {
      required: true,
      type: Array,
    },
    columnsSelected: {
      required: true,
      type: Array,
    },

    nameVuexModule: {
      required: true,
      type: String,
    },
    nameLocalStorageColumnsSelected: {
      required: true,
      type: String,
    },
    nameStateColumnsSelected: {
      required: true,
      type: String,
    },
    nameStateColumnsSelectedInitial: {
      required: true,
      type: String,
    },
  },
  data() {
    return {
      dialog: false,
      columnsSelectedIntern: this.columnsSelected,
    };
  },
  computed: {
    columnsSelectedInitial() {
      return this.$store.state[this.nameVuexModule][this.nameStateColumnsSelectedInitial];
    },
    isToggledAll: {
      get() {
        return _.size(this.columns) === _.size(this.columnsSelectedIntern);
      },
      set(isChecked) {
        if (isChecked === true) {
          this.columnsSelectedIntern = _.map(
            this.columns,
            column => column.value,
          );
        } else {
          this.columnsSelectedIntern = [];
        }
      },
    },
    is_indeterminate() {
      return (
        !this.isToggledAll && _.size(this.columnsSelectedIntern) !== 0
      );
    },
  },
  watch: {
    columnsSelectedIntern() {
      this.setArrayColumns(this.columnsSelectedIntern);
    },
  },
  methods: {
    setArrayColumns(columns) {
      this.$store.dispatch(`${this.nameVuexModule}/setState`, {
        objectState: columns,
        nameState: this.nameStateColumnsSelected,
        nameLocalStorage: this.nameLocalStorageColumnsSelected,
      });
    },
  },
};
</script>

<style scoped></style>
