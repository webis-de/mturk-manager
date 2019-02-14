<template>
  <div>
    <h1>Batches</h1>

    <v-text-field
      v-model="search"
      append-icon="search"
      label="Search"
      single-line
      hide-details
    ></v-text-field>

    <v-data-table
      v-bind:items="list_batches"
      v-bind:headers="list_headers"
      v-bind:search="search"
      v-model="batches_selected"
      disable-initial-sort
      select-all
      v-bind:pagination.sync="pagination"
      class="elevation-1"
    >
      <template slot="items" slot-scope="props">
        <td>
          <v-checkbox
            v-model="props.selected"
            primary
            hide-details
          ></v-checkbox>
        </td>
        <td>{{ props.item.id }}</td>
        <td>{{ props.item.datetime_creation.toLocaleString() }}</td>

        <td>
          <component-display-money
            v-bind:amount="props.item.settings_batch.reward"
          ></component-display-money>
        </td>
        <td>{{ props.item.hits.length }}</td>
        <td>{{ props.item.count_assignments_per_hit }}</td>
        <td>{{ props.item.count_assignments_total }}</td>
        <td>{{ props.item.count_assignments_approved }}</td>
        <td>{{ props.item.count_assignments_rejected }}</td>

        <td class="text-xs-right">
          <component-display-money
            v-bind:amount="
              show_with_fee
                ? props.item.money_spent_max_with_fee
                : props.item.money_spent_max_without_fee
            "
          ></component-display-money>
        </td>
        <td class="text-xs-right">
          <component-display-money
            v-bind:amount="
              show_with_fee
                ? props.item.money_spent_with_fee
                : props.item.money_spent_without_fee
            "
          ></component-display-money>
        </td>
      </template>
    </v-data-table>

    <v-btn
      :loading="is_downloading_csv"
      :disabled="is_downloading_csv"
      color="primary"
      @click.native="download_csv"
    >
      Download CSV for {{ count_hits_to_download }} HITs
      <v-icon right>cloud_download</v-icon>
    </v-btn>
    {{ batches_selected }}
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from "vuex";
import axios from "axios";
import Papa from "papaparse";
import _ from "lodash";
import ComponentDisplayMoney from "../base-display-amount.vue";

export default {
  name: "component-show-batches",
  data() {
    return {
      // set initial number of rows per page
      pagination: {
        rowsPerPage: 10
      },
      batches_selected: [],
      is_downloading_csv: false,
      search: "",
      list_headers: [
        {
          text: "ID",
          value: "id"
        },
        //     		{
        // 	text: 'HIT',
        // 	value: 'id_hit',
        // },
        //     		{
        // 	text: 'Assignment',
        // 	value: 'id_assignment',
        // },
        {
          text: "Created at",
          value: "datetime_creation"
        },
        {
          text: "Reward",
          value: "reward"
        },
        {
          text: "#HITs",
          value: "hits.length"
        },
        {
          text: "#Assignments per HIT",
          value: "count_assignments_per_hit"
        },
        {
          text: "#Assignments",
          value: "count_assignments_total"
        },
        {
          text: "#Approved assignments",
          value: "count_assignments_approved"
        },
        {
          text: "#Rejected assignments",
          value: "count_assignments_rejected"
        },
        {
          text: "Max costs",
          value: "money_spent_max_with_fee",
          align: "right"
        },
        {
          text: "Costs so far",
          value: "money_spent_with_fee",
          align: "right"
        }
      ]
    };
  },
  computed: {
    set_batches_selected: function() {
      if (this.batches_selected.length == 0) {
        return new Set(_.map(this.list_batches, o => o.id));
      } else {
        return new Set(_.map(this.batches_selected, o => o.id));
      }
    },
    count_hits_to_download: function() {
      if (this.batches_selected.length == 0) {
        return "all";
      } else {
        return _.sumBy(this.batches_selected, "hits.length");
      }
    },
    ...mapGetters("moduleBatches", {
      list_batches: "list_batches",
      list_hits_for_csv: "list_hits_for_csv"
    }),
    ...mapState(["show_with_fee"])
  },
  methods: {
    download_csv: function() {
      this.is_downloading_csv = true;

      // filter the selected hits
      const hits_selected = _.filter(this.list_hits_for_csv, hit =>
        this.set_batches_selected.has(hit[2])
      );
      console.log(hits_selected);
      const csv_string = Papa.unparse({
        fields: ["id_hit", "costs", "id_batch"],
        data: _.map(hits_selected, o => _.slice(o, 0, 2))
      });
      var blob = new Blob([csv_string]);
      var a = window.document.createElement("a");
      a.href = window.URL.createObjectURL(blob, { type: "text/plain" });
      a.download = "filename.csv";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      this.is_downloading_csv = false;
    }
  },
  components: {
    ComponentDisplayMoney
  }
};
</script>

<style lang="scss" scoped></style>
