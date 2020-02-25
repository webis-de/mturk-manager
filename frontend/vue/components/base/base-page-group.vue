<template>
  <v-row
    v-bind:id="identifier.identifier !== undefined ? identifier.identifier : false"
    dense
  >
    <base-wrap-node
      v-for="basePageSection in $slots.default"
      v-bind:value="basePageSection"
      v-bind:options="options(basePageSection)"
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
  methods: {
    options(node) {
      let classes = 'col py-0';

      if (node.componentOptions.propsData.shrink !== undefined) {
        classes += ' shrink';
      }

      return {
        attrs: {
          class: classes,
        },
      };
    },
  },
};
</script>

<style scoped>

</style>
