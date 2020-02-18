<template>
  <v-row
    v-bind:id="identifier.identifier !== undefined ? identifier.identifier : false"
    dense
  >
    <v-col
      v-for="basePageSection in $slots.default"
      class="py-0"
    >
      <base-wrap-node
        v-bind:value="basePageSection"
      />
    </v-col>
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
