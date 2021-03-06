<template>
  <base-table-item
    v-bind:key="assignment.id"
    v-bind:item="item"
    v-bind:items-selected="itemsSelected"
    v-on:changed-selection="$emit('changed-selection', $event)"
  >
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
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="hit"
      class="text-right"
      v-bind:item="assignment"
      v-bind:columns-selected="objectColumnsSelected"
      v-bind:to="{
        name: 'hit',
        params: {
          id: item.hit.id
        }
      }"
    >
      {{ item.hit.id_hit }}
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
      <v-btn
        x-small
        icon
        class="px-0"
        color="primary"
        v-on:click="annotate"
      >
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </base-table-cell>
  </base-table-item>
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
import BaseTableItem from '../../base-table-item';

export default {
  name: 'ComponentItemAssignment',
  components: {
    BaseTableItem,
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
    showLinks: {
      required: false,
      type: Boolean,
      default: true,
    },
    itemsSelected: {
      type: Object,
      required: true,
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
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  watch: {
    item() {
      // TODO: some other technique to prevent unnecessary updates?
      if (_.isEqual(this.assignment, this.item)) return;

      this.assignment = this.item;
    },
  },
  methods: {
    annotate() {
      window.open(`/view/${this.project_current.slug}?list_ids=[${this.assignment.id}]`, '_blank');
    },
    ...mapMutations('moduleAssignments', {
      set_assignments_selected: 'set_assignments_selected',
    }),
  },
};
</script>

<style lang="scss" scoped></style>
