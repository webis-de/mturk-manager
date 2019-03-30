<template>
  <v-flex
    v-bind="breakpoints"
  >
    <v-card
        v-bind:color="filtersActive.hasOwnProperty(nameFilter) ? 'secondary' : 'secondary'"
    >
      <v-card-title
        class="px-2 py-1"
      >
        <v-layout>
          <v-flex
            class="subheading"
          >
            <span
              v-bind:class="{
                'warning--text': filtersActive.hasOwnProperty(nameFilter)
              }"
            >
                {{ title }}
            </span>
          </v-flex>
          <v-flex
            shrink
          >
            <slot
              name="header"
            ></slot>
            <v-switch
              class="mt-0 pt-0"
              label="Exclude"
              hide-details
              v-bind:input-value="isExcluded"
              v-on:change="$set(filters, nameExcluded, $event)"
            />
          </v-flex>
        </v-layout>
      </v-card-title>
      <v-card-text
        class="px-2 pt-0 pb-2"
      >
        <slot></slot>
      </v-card-text>
    </v-card>
  </v-flex>

</template>

<script>
export default {
  name: 'BaseTableFilter',
  props: {
    filtersActive: {
      required: true,
      type: Object,
    },
    filters: {
      required: true,
      type: Object,
    },
    title: {
      required: true,
      type: String,
    },
    nameFilter: {
      required: true,
      type: String,
    },
    breakpoints: {
      required: false,
      type: Object,
      default: () => {},
    },
  },
  computed: {
    nameExcluded() {
      return `${this.nameFilter}Exclude`;
    },
    isExcluded() {
      return this.filters.hasOwnProperty(this.nameExcluded) ? this.filters[this.nameExcluded] : false;
    }
  }
};
</script>

<style scoped>

</style>