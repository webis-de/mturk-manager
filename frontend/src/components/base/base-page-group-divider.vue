<template>
  <h2
    v-bind:id="identifier.identifier !== null ? identifier.identifier : false"
    class="mt-8 display-1 ml-0"
  >
    <slot></slot>
  </h2>
</template>

<script>
export default {
  name: 'BasePageGroupDivider',
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
