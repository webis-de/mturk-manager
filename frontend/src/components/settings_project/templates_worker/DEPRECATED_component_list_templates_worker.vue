<template>
  <div>
    <v-data-table
      v-bind:headers="list_headers"
      v-bind:items="list_templates_worker"
    >
      <template slot="items" slot-scope="props">
        <tr>
          <td>
            {{ props.item.name }}
          </td>
          <td>{{ props.item.height_frame }} px</td>
          <td>
            {{ Object.keys(props.item.dict_parameters).length }}
          </td>
          <td>
            <span v-if="props.item.template_assignment == undefined">
              None
            </span>
            <span v-else>
              {{ props.item.template_assignment.name }}
            </span>
          </td>
          <td>
            <span v-if="props.item.template_hit == undefined">
              None
            </span>
            <span v-else>
              {{ props.item.template_hit.name }}
            </span>
          </td>
          <td>
            <span v-if="props.item.template_global == undefined">
              None
            </span>
            <span v-else>
              {{ props.item.template_global.name }}
            </span>
          </td>
          <td>
            <component-edit-template-worker
              v-bind:key="`component-edit-template-worker-${props.item.id}`"
              v-bind:template_worker_current="props.item"
              v-on:edited="snackbar_edited = true"
            ></component-edit-template-worker>
            <!-- <component-delete-template-worker
                        v-bind:key="`component-delete-template-worker-${props.item.id}`"
                        v-bind:template_worker="props.item"
                        v-on:deleted="snackbar_deleted = true"
                    ></component-delete-template-worker> -->
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
          <component-add-template-worker
            v-on:created="snackbar_created = true"
          ></component-add-template-worker>
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
import ComponentAddTemplateWorker from './component_add_template_worker.vue';
import ComponentEditTemplateWorker from './component_edit_template_worker.vue';
import ComponentDeleteTemplateWorker from './component_delete_template_worker.vue';

export default {
  name: 'component-list-templates-worker',
  data() {
    return {
      list_headers: [
        {
          text: 'Name',
          value: 'name',
        },
        {
          text: 'Height',
          value: 'height_frame',
        },
        {
          text: '#Variables',
          value: 'count_parameters',
        },
        {
          text: 'Assignment Template',
          value: 'template_assigmnent',
        },
        {
          text: 'Assignment HIT',
          value: 'template_hit',
        },
        {
          text: 'Assignment Global',
          value: 'template_global',
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
    list_templates_worker() {
      // return [{name:"dawd"}]
      if (this.project_current.templates_worker == null) return [];

      return _.orderBy(
        this.project_current.templates_worker,
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
    ComponentAddTemplateWorker,
    ComponentEditTemplateWorker,
    ComponentDeleteTemplateWorker,
  },
};
</script>
