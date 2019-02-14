<template>
  <!-- <div>wda</div> -->
  <tr
    v-bind:key="assignment.id"
    v-on:click="props.expanded = !props.expanded"
    class="text-no-wrap"
  >
    <td v-bind:style="stylesCell">
      <v-checkbox v-model="is_selected" primary hide-details></v-checkbox>
    </td>
    <td
      v-if="set_columns_selected.has('id_assignment')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      {{ assignment.id_assignment }}
    </td>
    <td
      v-if="set_columns_selected.has('datetime_creation')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      <component-display-datetime
        v-bind:datetime="assignment.datetime_creation"
      ></component-display-datetime>
    </td>
    <td
      v-if="set_columns_selected.has('datetime_accept')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      <component-display-datetime
        v-bind:datetime="assignment.datetime_accept"
      ></component-display-datetime>
    </td>
    <td
      v-if="set_columns_selected.has('datetime_submit')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      <component-display-datetime
        v-bind:datetime="assignment.datetime_submit"
      ></component-display-datetime>
    </td>
    <td
      v-if="set_columns_selected.has('duration')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      <component-display-duration
        v-bind:duration="assignment.duration"
      ></component-display-duration>
    </td>
    <td
      v-if="set_columns_selected.has('worker')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      {{ assignment.worker.id_worker }}
    </td>
    <td
      v-if="set_columns_selected.has('status')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      <component-status-assignment
        v-bind:assignment="assignment"
      ></component-status-assignment>
    </td>
    <td
      v-if="set_columns_selected.has('hit')"
      class="text-xs-right"
      v-bind:style="stylesCell"
    >
      {{ assignment.hit.id_hit }}
      <v-btn
        slot="activator"
        class="my-0"
        icon
        small
        v-bind:to="{
          name: 'hit',
          params: {
            slug_project: $route.params.slug_project,
            id_hit: assignment.hit.id
          }
        }"
      >
        <v-icon>info</v-icon>
      </v-btn>
    </td>
    <td
      class="text-xs-center"
      v-if="show_links === false"
      v-bind:style="stylesCell"
    >
      <v-btn
        slot="activator"
        class="my-0"
        icon
        small
        v-bind:to="{
          name: 'assignment',
          params: {
            slug_project: $route.params.slug_project,
            id_assignment: assignment.id
          }
        }"
      >
        <v-icon>info</v-icon>
      </v-btn>
    </td>
    <!-- <td class="text-xs-center">
            {{ assignment.hits.length }}
        </td>
        <td class="text-xs-center">
            {{ props.item.count_assignments }}
        </td> -->
  </tr>
</template>
<script>
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";
import _ from "lodash";
import ComponentDisplayDatetime from "../../helpers/component_display_datetime";
import ComponentStatusAssignment from "./component-status-assignment";
import ComponentDisplayDuration from "../../helpers/component-display-duration";

export default {
  name: "component-item-assignment",
  props: {
    props: {
      type: Object,
      required: true
    },
    show_links: {
      required: false,
      type: Boolean,
      default: true
    },
    array_columns_selected: {
      type: Array,
      required: true
    },

    isCondensed: {
      required: true,
      type: Boolean
    }
  },
  data() {
    return {};
  },
  // watch: {
  //     'worker.is_blocked': function() {
  //         console.log(this.worker.is_blocked)
  //     },
  // },
  computed: {
    set_columns_selected() {
      return new Set(this.array_columns_selected);
    },
    is_selected: {
      get() {
        return _.has(this.object_assignments_selected, this.assignment.id);
      },
      set(is_selected) {
        this.set_assignments_selected({
          array_items: [this.assignment],
          add: is_selected
        });
      }
    },
    assignment() {
      return this.props.item;
    },
    stylesCell() {
      if (this.isCondensed) {
        return {
          height: "unset !important",
          paddingLeft: "5px !important",
          paddingRight: "5px !important"
        };
      } else {
        return {};
      }
    },
    ...mapGetters("moduleAssignments", {
      object_assignments_selected: "get_object_assignments_selected"
    }),
    ...mapGetters(["get_show_progress_indicator"])
  },
  methods: {
    ...mapMutations("moduleAssignments", {
      set_assignments_selected: "set_assignments_selected"
    })
  },
  components: {
    ComponentDisplayDuration,
    ComponentStatusAssignment,
    ComponentDisplayDatetime
  }
};
</script>

<style lang="scss" scoped></style>
