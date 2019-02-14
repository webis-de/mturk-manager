<template>
  <div>
    <v-data-table
      v-bind:headers="list_headers"
      v-bind:items="list_templates_assignment"
    >
      <template slot="items" slot-scope="props">
        <tr>
          <td>
            {{ props.item.name }}
          </td>
          <td>
            <component-edit-template-assignment
              v-bind:key="`component-edit-template-assignment-${props.item.id}`"
              v-bind:template_assignment_current="props.item"
              v-on:edited="snackbar_edited = true"
            ></component-edit-template-assignment>
            <component-delete-template-assignment
              v-bind:key="
                `component-delete-template-assignment-${props.item.id}`
              "
              v-bind:template_assignment="props.item"
              v-on:deleted="snackbar_deleted = true"
            ></component-delete-template-assignment>
          </td>
        </tr>
      </template>
      <template slot="no-data">
        <div class="text-xs-center">
          There exist no templates!
        </div>
      </template>
      <template slot="footer">
        <td colspan="100%">
          <component-add-template-assignment
            v-on:created="snackbar_created = true"
          ></component-add-template-assignment>
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
import ComponentAddTemplateAssignment from "./component_add_template_assignment.vue";
import ComponentDeleteTemplateAssignment from "./component_delete_template_assignment.vue";
import ComponentEditTemplateAssignment from "./component_edit_template_assignment.vue";
import { table } from "../../../mixins/table";

export default {
  mixins: [table],
  name: "component-list-templates-assignment",
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
      snackbar_edited: false,
      snackbar_created: false
    };
  },
  computed: {
    list_templates_assignment() {
      // return [{name:"dawd"}]
      if (this.project_current.templates_assignment == null) return [];

      return _.orderBy(
        this.project_current.templates_assignment,
        template => template.name
      );
    },
    ...mapGetters("moduleProjects", {
      project_current: "get_project_current"
    })
  },
  methods: {},
  created: function() {},
  components: {
    ComponentAddTemplateAssignment,
    ComponentDeleteTemplateAssignment,
    ComponentEditTemplateAssignment
  }
};
</script>
