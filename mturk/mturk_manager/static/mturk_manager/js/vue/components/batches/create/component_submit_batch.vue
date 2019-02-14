<template>
  <v-layout wrap>
    <v-flex>
      <v-btn
        class="mx-3"
        v-bind:disabled="!is_valid"
        v-bind:loading="is_uploading_batch"
        large
        color="success"
        v-on:click="submit"
        >Submit Batch</v-btn
      >
    </v-flex>
  </v-layout>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import Settings_Batch from "../../../classes/settings_batch";
import { Service_Batches } from "../../../services/service_batches";

export default {
  name: "component-submit-batch",
  props: {
    settings_batch_current: {
      required: true,
      type: Settings_Batch | undefined
    },
    is_invalid_settings_batch: {
      required: true,
      type: Boolean
    },
    name_batch: {
      required: true,
      type: String | undefined
    },
    is_creating_batch: {}
  },
  data() {
    return {
      is_uploading_batch: false
    };
  },
  computed: {
    is_valid() {
      return this.is_valid_csv && !this.is_invalid_settings_batch;
    },
    ...mapGetters("moduleProjects", {
      // 'project_current': 'get_project_current',
    }),
    ...mapGetters("moduleBatches", {
      object_csv_parsed: "get_object_csv_parsed",
      is_valid_csv: "is_valid_csv"
    })
  },
  methods: {
    submit() {
      this.is_uploading_batch = true;
      console.log("adding batch");

      Service_Batches.create({
        name: this.name_batch,
        settings_batch: this.settings_batch_current,
        data_csv: this.object_csv_parsed.data
      }).then(() => {
        this.is_uploading_batch = false;
        this.$emit("update:is_creating_batch", false);
        Service_Batches.load_page({
          page: 1,
          rowsPerPage: 25,
          sortBy: "datetime_creation"
        });
      });
    }
  }
};
</script>

<style lang="css" scoped></style>
