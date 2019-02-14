<template>
  <!-- <div>wda</div> -->
  <tr v-bind:key="batch.id" class="text-no-wrap">
    <td v-bind:style="stylesCell">
      <v-checkbox v-model="is_selected" primary hide-details></v-checkbox>
    </td>

    <td
      v-if="set_columns_selected.has('name')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      {{ batch.name.toUpperCase() }}
    </td>

    <td
      v-if="set_columns_selected.has('count_hits')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      {{ batch.count_hits }}
    </td>

    <td
      v-if="set_columns_selected.has('datetime_creation')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      <component-display-datetime v-bind:datetime="batch.datetime_creation">
      </component-display-datetime>
    </td>

    <td
      v-if="set_columns_selected.has('settings_batch__count_assignments')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      {{ batch.settings_batch.count_assignments }}
    </td>

    <td
      v-if="set_columns_selected.has('settings_batch__reward')"
      class="text-xs-right"
      v-bind:style="stylesCell"
    >
      <base-display-amount
        v-bind:amount="batch.settings_batch.reward"
      ></base-display-amount>
    </td>

    <td
      v-if="set_columns_selected.has('count_assignments_total')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      {{ batch.count_assignments_total }}
    </td>

    <td
      v-if="set_columns_selected.has('count_assignments_approved')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      {{ batch.count_assignments_approved }}
    </td>

    <td
      v-if="set_columns_selected.has('count_assignments_rejected')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      {{ batch.count_assignments_rejected }}
    </td>

    <td
      v-if="set_columns_selected.has('costs_max')"
      class="text-xs-right"
      v-bind:style="stylesCell"
    >
      <base-display-amount
        v-bind:amount="batch.costs_max"
      ></base-display-amount>
    </td>

    <td
      v-if="set_columns_selected.has('costs_so_far')"
      class="text-xs-right"
      v-bind:style="stylesCell"
    >
      <base-display-amount
        v-bind:amount="batch.costs_so_far"
      ></base-display-amount>
    </td>

    <td
      v-if="set_columns_selected.has('progress')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      <component-batch-progress v-bind:progress="batch.progress">
        {{ batch.count_assignments_available }}/{{
          batch.count_assignments_total
        }}
        assignment{{ batch.count_assignments_total > 1 ? "s" : "" }}
      </component-batch-progress>
    </td>

    <td
      v-if="set_columns_selected.has('actions')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      <v-btn
        slot="activator"
        class="my-0"
        icon
        small
        v-bind:to="{
          name: 'batch',
          params: {
            slug_project: $route.params.slug_project,
            id_batch: batch.id
          }
        }"
      >
        <v-icon>info</v-icon>
      </v-btn>
    </td>
  </tr>
</template>
<script>
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";
import _ from "lodash";
import ComponentBatchProgress from "./component_batch_progress.vue";
import ComponentDisplayDatetime from "../../helpers/component_display_datetime.vue";
import BaseDisplayAmount from "../../base-display-amount";

export default {
  name: "component-item-batch",
  props: {
    props: {
      required: true
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
  computed: {
    is_selected: {
      get() {
        return _.has(this.object_batches_selected, this.batch.id);
      },
      set(is_selected) {
        this.set_batches_selected({
          array_items: [this.batch],
          add: is_selected
        });
      }
    },
    set_columns_selected() {
      return new Set(this.array_columns_selected);
    },
    batch() {
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
    ...mapGetters(["get_show_progress_indicator"]),
    ...mapGetters("moduleBatches", {
      object_batches_selected: "get_object_batches_selected"
    })
  },
  methods: {
    ...mapMutations("moduleBatches", {
      set_batches_selected: "set_batches_selected"
    })
  },
  mounted() {},
  components: {
    BaseDisplayAmount,
    ComponentBatchProgress,
    ComponentDisplayDatetime
  }
};
</script>

<style lang="scss" scoped></style>
