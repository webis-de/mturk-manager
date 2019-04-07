<template>
  <v-layout wrap>
    <v-flex>
      <v-layout wrap>
        <v-flex class="text-xs-center">
          <div class="headline">Open Existing Project</div>
        </v-flex>
      </v-layout>
      <v-layout wrap>
        <v-flex>
          <v-text-field
            v-model="search"
            append-icon="search"
            label="Search for Project"
            hide-details
            class="mb-2"
          ></v-text-field>
        </v-flex>
      </v-layout>
      <v-layout wrap>
        <v-flex>
          <!-- select-all -->
          <!-- v-bind:rows-per-page-items="items_per_page" -->
          <!-- select-all -->
          <v-data-table
            v-bind:pagination.sync="pagination"
            v-bind:headers="list_headers"
            v-bind:items="list_projects"
            v-bind:search="search"
          >
            <template slot="items" slot-scope="props">
              <tr v-bind:key="props.item.id">
                <td>
                  {{ props.item.name }}
                </td>
                <td>
                  <base-display-datetime
                    v-bind:datetime="props.item.datetime_visited"
                  ></base-display-datetime>
                </td>
                <td class="text-xs-right">
                  <!-- v-bind:to="{ name: 'batches', params: { slug_project: props.item.slug } }" -->
                  <v-btn
                    small
                    color="primary"
                    v-bind:to="{
                      name: 'project',
                      params: { slug_project: props.item.slug }
                    }"
                    >Open</v-btn
                  >
                  <!-- v-bind:to="{ name: 'batches', params: { slug_project: props.item.slug } }" -->
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import _ from 'lodash';
import { table } from '../../mixins/table';
import BaseDisplayDatetime from '../common/base-display-datetime';

export default {
  mixins: [table],
  name: 'component-open-project',
  data() {
    return {
      search: '',
      list_headers: [
        {
          text: 'Name',
          value: 'name',
          align: 'left',
        },
        {
          text: 'Last Usage',
          value: 'datetime_visited',
          align: 'left',
        },
        {
          text: '',
          value: '',
          align: '',
          sortable: false,
        },
      ],
      pagination: {
        sortBy: 'datetime_visited',
        descending: true,
      },
    };
  },
  computed: {
    list_projects() {
      return _.orderBy(this.object_projects, ['datetime_visited'], ['desc']);
    },
    ...mapGetters('moduleProjects', {
      object_projects: 'get_object_projects',
    }),
  },
  methods: {},
  created() {},
  components: {
    BaseDisplayDatetime
  },
};
</script>
