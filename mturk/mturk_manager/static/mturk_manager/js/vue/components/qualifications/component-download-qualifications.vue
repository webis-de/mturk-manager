<template>
  <v-btn color="info" class="mb-2" v-on:click.native="download">
    <v-icon left>cloud_download</v-icon>{{ title_button }}
  </v-btn>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import _ from "lodash";

export default {
  name: "component-download-qualifications",
  props: {
    qualifications_selected: {
      type: Array,
      required: true
    }
  },
  data() {
    return {};
  },
  computed: {
    title_button: function() {
      if (this.qualifications_selected_without_database_entry.length == 0) {
        return `Download all (${
          this.qualifications_without_database_entry.length
        }) Qualification(s)`;
      } else {
        return `Download ${
          this.qualifications_selected_without_database_entry.length
        } Qualification(s)`;
      }
    },
    qualifications_selected_without_database_entry: function() {
      return _.filter(this.qualifications_selected, q =>
        q.has_database_entry()
      );
    },
    qualifications_without_database_entry: function() {
      return _.filter(this.list_policies, q => q.has_database_entry());
    },
    ...mapGetters("moduleQualifications", {
      list_policies: "list_policies"
    })
  },
  methods: {
    download: function() {
      const array_json = [];
      if (this.qualifications_selected_without_database_entry.length == 0) {
        for (
          let i = 0;
          i < this.qualifications_without_database_entry.length;
          i++
        ) {
          array_json.push(
            this.qualifications_without_database_entry[i].get_json()
          );
        }
      } else {
        for (
          let i = 0;
          i < this.qualifications_selected_without_database_entry.length;
          i++
        ) {
          array_json.push(
            this.qualifications_selected_without_database_entry[i].get_json()
          );
        }
      }

      this.download_file(array_json.join("\n"), {
        name: "qualifications.json",
        type: "application/json"
      });
    },
    download_file(string) {
      const options =
        arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

      if (options.name === undefined) options.name = "file.json";
      if (options.type === undefined) options.type = "text/plain";

      const blob = new Blob([string], { type: options.type });
      const link_virtual = window.document.createElement("a");
      link_virtual.href = window.URL.createObjectURL(blob);
      link_virtual.download = options.name;
      document.body.appendChild(link_virtual);
      link_virtual.click();
      document.body.removeChild(link_virtual);
    }
  }
};
</script>
