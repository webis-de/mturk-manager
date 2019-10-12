<template>
  <v-row no-gutters>
    <v-col>
      <v-row no-gutters>
        <v-col>
          <div class="headline">
            Open Existing Project
          </div>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search for Project"
            hide-details
            class="mb-2"
            clearable
          />
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col>
          <!-- select-all -->
          <!-- v-bind:rows-per-page-items="items_per_page" -->
          <!-- select-all -->
          <v-data-table
            v-bind:headers="listHeaders"
            v-bind:items="listProjects"
            v-bind:search="search"
            sort-by="datetime_visited"
            v-bind:sort-desc="true"
          >
            <template v-slot:item.datetime_visited="{ value }">
              <base-display-datetime
                v-bind:datetime="value"
              />
            </template>
            <template v-slot:item.actions="{ item }">
              <v-btn
                small
                color="primary"
                v-bind:to="{
                  name: 'project',
                  params: { slug_project: item.slug }
                }"
              >
                Open
              </v-btn>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from 'vuex';
import { compareAsc } from 'date-fns';
import BaseDisplayDatetime from '../common/base-display-datetime';

export default {
  name: 'OpenProject',
  components: {
    BaseDisplayDatetime,
  },
  data() {
    return {
      search: '',
      listHeaders: [
        {
          text: 'Name',
          value: 'name',
          align: 'left',
        },
        {
          text: 'Last Usage',
          value: 'datetime_visited',
          align: 'left',
          sort: (a, b) => {
            return compareAsc(a, b);
          },
        },
        {
          text: '',
          value: 'actions',
          align: '',
          sortable: false,
        },
      ],
    };
  },
  computed: {
    listProjects() {
      return Object.values(this.objectProjects);
    },
    ...mapGetters('moduleProjects', {
      objectProjects: 'get_object_projects',
    }),
  },
};
</script>
