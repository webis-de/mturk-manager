<template>
  <v-row
    v-bind:id="identifier"
    dense
  >
    <v-col v-if="type === 'table'">
      <slot></slot>
    </v-col>
    <v-col v-else>
      <slot></slot>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'BasePageSection',
  props: {
    type: {
      type: String,
      required: true,
    },
    identifier: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>

</style>
