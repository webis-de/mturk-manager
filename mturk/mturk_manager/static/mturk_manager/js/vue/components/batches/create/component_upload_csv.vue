<template>
  <v-layout>
    <v-flex>
      <v-layout>
        <v-flex shrink>
          <upload-btn
            class="pl-0"
            :file-changed-callback="file_changed"
            title="Upload CSV"
            v-bind:loading="is_parsing_csv"
          ></upload-btn>
        </v-flex>
        <v-flex align-self-center>
          {{ tmp_name_file }}
        </v-flex>
      </v-layout>

      <v-dialog v-model="is_parsing_csv" hide-overlay persistent width="300">
        <v-card color="primary" dark>
          <v-card-text>
            Parsing CSV...
            <v-progress-linear
              indeterminate
              color="white"
              class="mb-0"
            ></v-progress-linear>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-flex>
  </v-layout>
</template>

<script>
import { mapState, mapMutations, mapActions, mapGetters } from "vuex";
import UploadButton from "vuetify-upload-button";
import Papa from "papaparse";

// import ComponentStepUploadCSV from './component_step_upload_csv.vue';
// import ComponentShowMoneySpent from './component-show-money-spent.vue';
// import ComponentShowBatches from './component-show-batches.vue';
export default {
  name: "component-upload-csv",
  props: {},
  data() {
    return {
      file_csv: null,
      is_parsing_csv: false
    };
  },
  mounted() {
    // this.set_csv_parsed({ "data": [ { "link_1": "http://webislab35.medien.uni-weimar.de:8002/wiki/Margaret_Billingham", "link_2": "http://webislab35.medien.uni-weimar.de:8002/wiki/Benik_Afobe", "link_3": "http://webislab35.medien.uni-weimar.de:8002/wiki/Letter_to_Blanchy" } ], "errors": [], "meta": { "delimiter": ",", "linebreak": "\r\n", "aborted": false, "truncated": false, "cursor": 220, "fields": [ "link_1", "link_2", "link_3" ] } });
  },
  methods: {
    file_changed(file) {
      this.file_csv = file;

      if (file == null) {
        this.reset();
        return;
      }

      this.is_parsing_csv = true;
      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: (results, file) => {
          console.log("results", results);
          this.is_parsing_csv = false;
          this.set_csv_parsed(results);
        }
      });
    },
    reset() {
      this.file_csv = null;
      this.is_parsing_csv = false;
      this.set_csv_parsed(undefined);
    },
    ...mapMutations("moduleBatches", {
      set_csv_parsed: "set_csv_parsed"
    })
  },
  computed: {
    tmp_name_file() {
      if (this.file_csv != null) {
        return this.file_csv.name;
      }
      return null;
    },
    ...mapGetters("moduleBatches", {
      get_object_csv_parsed: "get_object_csv_parsed",
      is_valid_csv: "is_valid_csv"
    })
  },
  components: {
    "upload-btn": UploadButton
  }
};
</script>

<style scoped>
input[type="file"] {
  position: absolute;
  left: -99999px;
}
</style>
