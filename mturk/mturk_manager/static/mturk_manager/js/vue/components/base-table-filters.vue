<template>
  <v-bottom-sheet
    v-model="showFilters"
    hide-overlay
    inset
  >
    <template v-slot:activator>
      <v-btn
        v-if="countFiltersActive === 0"

        small
        color="primary"
      >
        Filters
      </v-btn>
      <v-btn
        v-else

        small
        color="warning"
      >
        Filters ({{ countFiltersActive }})
      </v-btn>
    </template>

    <v-card
      color="secondary darken-1"
    >
      <v-card-title
        class="pa-2"
      >
        <v-layout>
          <v-flex align-self-center>
            <span class="title">
              Filters
            </span>
          </v-flex>
          <v-flex
            shrink
            class="pr-4"
          >
            <span
              v-if="countFiltersActive > 0"
              class="warning--text text-uppercase"
            >
              {{ countFiltersActive }} active filter(s)
            </span>
            <v-btn
              small
              flat
              class="ma-0"
              color="primary"
              v-on:click.stop="resetFilters()"
            >
              Reset
            </v-btn>
          </v-flex>
        </v-layout>
      </v-card-title>
      <v-card-text>
        <v-container
          class="pa-0"
          grid-list-md
          fluid
        >
          <slot
            name="filters"
            v-bind:filters="filtersCloned"
            v-bind:filters-active="filtersActive"
          />
        </v-container>
      </v-card-text>
    </v-card>
  </v-bottom-sheet>

  <!--<v-expansion-panel-->
    <!--v-model="showFilters"-->
    <!--class="mb-1"-->
  <!--&gt;-->
    <!--<v-expansion-panel-content>-->
      <!--<template v-slot:header>-->
        <!--<v-layout>-->
          <!--<v-flex align-self-center>-->
            <!--<span class="title">Filters</span>-->
          <!--</v-flex>-->
          <!--<v-flex-->
            <!--shrink-->
            <!--class="pr-4"-->
          <!--&gt;-->
            <!--<span-->
              <!--v-if="countFiltersActive > 0"-->
              <!--class="warning&#45;&#45;text text-uppercase"-->
            <!--&gt;-->
              <!--{{ countFiltersActive }} active filter(s)-->
            <!--</span>-->
            <!--<v-btn-->
              <!--small-->
              <!--flat-->
              <!--class="ma-0"-->
              <!--color="primary"-->
              <!--v-on:click.stop="resetFilters()"-->
            <!--&gt;-->
              <!--Reset-->
            <!--</v-btn>-->
          <!--</v-flex>-->
        <!--</v-layout>-->
      <!--</template>-->
      <!--<v-container-->
        <!--class="pt-0"-->
        <!--grid-list-md-->
        <!--fluid-->
      <!--&gt;-->
        <!--<slot-->
          <!--name="filters"-->
          <!--v-bind:filters="filtersCloned"-->
          <!--v-bind:filters-active="filtersActive"-->
        <!--/>-->
      <!--</v-container>-->
    <!--</v-expansion-panel-content>-->
  <!--</v-expansion-panel>-->
</template>

<script>
import {mapMutations} from 'vuex';

export default {
  name: 'BaseTableFilters',
  props: {
    filters: {
      required: false,
      type: Object,
      default: () => {},
    },
    filtersDefault: {
      required: false,
      type: Object,
      default: () => {},
    },
    nameStateFilters: {
      required: true,
      type: String,
    },
    nameLocalStorageFilters: {
      required: true,
      type: String,
    },
  },
  data() {
    return {
      showFilters: false,
      filtersCloned: _.cloneDeep(this.filters),
    };
  },
  computed: {
    countFiltersActive() {
      return Object.keys(this.filtersActive).length;
    },
    filtersActive() {
      return _.omitBy(this.filtersCloned, (value, key) => {
        if (this.filtersDefault[key] === undefined) {
          return true;
        }

        return _.isEqual(this.filtersDefault[key], value);
      });
    },
  },
  watch: {
    filtersCloned: {
      handler() {
        this.$emit('filtersChanged', this.filtersCloned);
        this.setState({
          objectState: this.filtersCloned,
          nameState: this.nameStateFilters,
          nameLocalStorage: this.nameLocalStorageFilters,
        });
      },
      deep: true,
    },
  },
  methods: {
    resetFilters() {
      this.filtersCloned = _.cloneDeep(this.filtersDefault);
    },
    ...mapMutations('moduleWorkers', ['setState']),
  },
};
</script>

<style scoped>

</style>