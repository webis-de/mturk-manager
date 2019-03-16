<template>
  <v-flex
    v-bind="breakpoints"
  >
    <v-card
      v-bind:color="filtersActive.hasOwnProperty(nameFilter) ? 'secondary darken-1' : 'secondary'"
    >
      <v-card-title
        class="px-2 py-1"
      >
        <v-layout>
          <v-flex
            class="subheading"
          >
            {{ title }}
          </v-flex>
          <v-flex
            shrink
          >
            <slot
              name="header"
            ></slot>
            <!--<v-switch-->
              <!--class="mt-0 pt-0"-->
              <!--label="Exclude"-->
              <!--hide-details-->
            <!--/>-->
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
  }
};
</script>

<style scoped>

</style>