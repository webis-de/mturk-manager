<template>
  <!-- <div>wda</div> -->
  <tr
    v-bind:key="assignment.id"
    class="text-no-wrap"
  >
    <td>
      <v-checkbox
        v-model="is_selected"
        class="pa-0 ma-0"
        primary
        hide-details
      />
    </td>

    <base-table-cell
      v-slot="{ item }"
      name="id_assignment"
      class="text-left"
      v-bind:item="assignment"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.id_assignment }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="datetime_creation"
      class="text-center"
      v-bind:item="assignment"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <base-display-datetime
        v-bind:datetime="item.datetime_creation"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="datetime_accept"
      class="text-center"
      v-bind:item="assignment"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <base-display-datetime
        v-bind:datetime="item.datetime_accept"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="datetime_submit"
      class="text-center"
      v-bind:item="assignment"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <base-display-datetime
        v-bind:datetime="item.datetime_submit"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="duration"
      class="text-center"
      v-bind:item="assignment"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <base-display-duration
        v-bind:start="item.datetime_accept"
        v-bind:end="item.datetime_submit"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="worker"
      class="text-center"
      v-bind:item="assignment"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.worker.id_worker }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="status"
      class="text-center"
      v-bind:item="assignment"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <component-status-assignment
        v-bind:assignment="item"
      ></component-status-assignment>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="hit"
      class="text-right"
      v-bind:item="assignment"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.hit.id_hit }}
      <v-btn
        slot="activator"
        class="my-0"
        icon
        small
        v-bind:to="{
          name: 'hit',
          params: {
            slug_project: $route.params.slug_project,
            id: item.hit.id
          }
        }"
      >
        <v-icon>mdi-information</v-icon>
      </v-btn>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="actions"
      class="text-center"
      v-bind:item="assignment"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <edit-assignment
        v-bind:assignment="item"
      />
    </base-table-cell>

    <!-- <td class="text-xs-center">
            {{ assignment.hits.length }}
        </td>
        <td class="text-xs-center">
            {{ props.item.count_assignments }}
        </td> -->
  </tr>
</template>
<script>
import {
  mapState, mapActions, mapMutations, mapGetters,
} from 'vuex';
import _ from 'lodash';
import ComponentStatusAssignment from './component-status-assignment';
import BaseDisplayDatetime from '../../common/base-display-datetime';
import BaseDisplayDuration from '../../common/base-display-duration';
import BaseTableCell from '../../base-table-cell';
import EditAssignment from '../edit-assignment';

export default {
  name: 'ComponentItemAssignment',
  components: {
    EditAssignment,
    BaseTableCell,
    BaseDisplayDuration,
    BaseDisplayDatetime,
    ComponentStatusAssignment,
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
    show_links: {
      required: false,
      type: Boolean,
      default: true,
    },
    objectColumnsSelected: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      assignment: this.item,
    };
  },
  // watch: {
  //     'worker.is_blocked': function() {
  //         console.log(this.worker.is_blocked)
  //     },
  // },
  computed: {
    is_selected: {
      get() {
        return _.has(this.object_assignments_selected, this.assignment.id);
      },
      set(is_selected) {
        this.set_assignments_selected({
          array_items: [this.assignment],
          add: is_selected,
        });
      },
    },
    // assignment() {
    //   return this.props.item;
    // },
    ...mapGetters('moduleAssignments', {
      object_assignments_selected: 'get_object_assignments_selected',
    }),
    ...mapGetters(['get_show_progress_indicator']),
  },
  watch: {
    item() {
      // TODO: some other technique to prevent unnecessary updates?
      if (_.isEqual(this.assignment, this.item)) return;

      this.assignment = this.item;
    },
  },
  methods: {
    ...mapMutations('moduleAssignments', {
      set_assignments_selected: 'set_assignments_selected',
    }),
  },
};
</script>

<style lang="scss" scoped></style>
