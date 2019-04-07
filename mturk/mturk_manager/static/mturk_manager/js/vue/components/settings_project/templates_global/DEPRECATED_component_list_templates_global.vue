<template>
  <div>
    <v-data-table
      v-bind:headers="list_headers"
      v-bind:items="list_templates_global"
    >
      <template slot="items" slot-scope="props">
        <tr>
          <td>
            {{ props.item.name }}
          </td>
          <td>
            <component-edit-template-global
              v-bind:key="`component-edit-template-global-${props.item.id}`"
              v-bind:template_global_current="props.item"
              v-on:edited="snackbar_edited = true"
            ></component-edit-template-global>
            <component-delete-template-global
              v-bind:key="`component-delete-template-global-${props.item.id}`"
              v-bind:template_global="props.item"
              v-on:deleted="snackbar_deleted = true"
            ></component-delete-template-global>
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
          <component-add-template-global
            v-on:created="snackbar_created = true"
          ></component-add-template-global>
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
import { mapState, mapActions, mapGetters } from 'vuex';
import _ from 'lodash';
import ComponentAddTemplateGlobal from './component_add_template_global.vue';
import ComponentDeleteTemplateGlobal from './component_delete_template_global.vue';
import ComponentEditTemplateGlobal from './component_edit_template_global.vue';

export default {
  name: 'component-list-templates-global',
  data() {
    return {
      list_headers: [
        {
          text: 'Name',
          value: 'name',
        },
        {
          text: 'Actions',
          value: '',
          sortable: false,
        },
      ],

      snackbar_deleted: false,
      snackbar_edited: false,
      snackbar_created: false,
    };
  },
  computed: {
    list_templates_global() {
      // return [{name:"dawd"}]
      if (this.project_current.templates_global == null) return [];

      return _.orderBy(
        this.project_current.templates_global,
        template => template.name,
      );
    },
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  methods: {},
  created() {},
  components: {
    ComponentAddTemplateGlobal,
    ComponentDeleteTemplateGlobal,
    ComponentEditTemplateGlobal,
  },
};
</script>
