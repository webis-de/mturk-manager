<template>
  <v-row
    v-bind:id="identifier.identifier !== undefined ? identifier.identifier : false"
    dense
  >
    <base-wrap-node
      v-for="basePageSection in $slots.default"
      v-bind:value="basePageSection"
      v-bind:options="{
        attrs: {
          class: 'col py-0',
        }
      }"
    />
  </v-row>
</template>

<script>
import BaseWrapNode from './base-wrap-node';

export default {
  name: 'BasePageGroup',
  components: { BaseWrapNode },
  props: {
    identifier: {
      type: Object,
      required: false,
      default() {
        return {};
      },
    },
  },
};
</script>

<style scoped>

</style>
