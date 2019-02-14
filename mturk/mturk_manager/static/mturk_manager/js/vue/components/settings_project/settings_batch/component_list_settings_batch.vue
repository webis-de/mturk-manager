<template>
  <div>
    <v-data-table
      v-bind:headers="list_headers"
      v-bind:items="list_settings_batch"
    >
      <template slot="items" slot-scope="props">
        <tr>
          <td>
            {{ props.item.name }}
          </td>
          <td>
            <component-edit-settings-batch
              v-bind:key="`component-edit-settings-batch-${props.item.id}`"
              v-bind:settings_batch_current="props.item"
              v-on:edited="snackbar_edited = true"
            ></component-edit-settings-batch>
            <component-delete-settings-batch
              v-bind:key="`component-delete-settings-batch-${props.item.id}`"
              v-bind:settings_batch_current="props.item"
              v-on:deleted="snackbar_deleted = true"
            ></component-delete-settings-batch>
          </td>
        </tr>
      </template>
      <template slot="no-data">
        <div class="text-xs-center">
          There exist no profiles!
        </div>
      </template>
      <template slot="footer">
        <td colspan="100%">
          <component-add-settings-batch
            v-on:created="snackbar_created = true"
          ></component-add-settings-batch>
        </td>
      </template>
    </v-data-table>

    <v-snackbar v-model="snackbar_deleted" v-bind:timeout="1500" bottom>
      <v-spacer></v-spacer>
      Deleted!
      <v-spacer></v-spacer>
    </v-snackbar>

    <v-snackbar
      v-model="snackbar_created"
      v-bind:timeout="1500"
      bottom
      color="success"
    >
      <v-spacer></v-spacer>
      Saved!
      <v-spacer></v-spacer>
    </v-snackbar>

    <v-snackbar
      v-model="snackbar_edited"
      v-bind:timeout="1500"
      bottom
      color="success"
    >
      <v-spacer></v-spacer>
      Updated!
      <v-spacer></v-spacer>
    </v-snackbar>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
import _ from "lodash";
import ComponentAddSettingsBatch from "./component_add_settings_batch.vue";
import ComponentEditSettingsBatch from "./component_edit_settings_batch.vue";
import ComponentDeleteSettingsBatch from "./component_delete_settings_batch.vue";
import { table } from "../../../mixins/table";

export default {
  mixins: [table],
  name: "component-list-settings-batch",
  data() {
    return {
      list_headers: [
        {
          text: "Name",
          value: "name"
        },
        {
          text: "Actions",
          value: "",
          sortable: false
        }
      ],

      snackbar_deleted: false,
      snackbar_created: false,
      snackbar_edited: false
    };
  },
  computed: {
    list_settings_batch() {
      // return [{name:"dawd"}]
      if (this.project_current.settings_batch == null) return [];

      return _.orderBy(
        this.project_current.settings_batch,
        settings => settings.name
      );
    },
    ...mapGetters("moduleProjects", {
      project_current: "get_project_current"
    })
  },
  methods: {},
  created: function() {},
  components: {
    ComponentAddSettingsBatch,
    ComponentEditSettingsBatch,
    ComponentDeleteSettingsBatch
  }
};
</script>
