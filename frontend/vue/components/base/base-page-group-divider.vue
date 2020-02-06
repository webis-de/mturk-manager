<template>
  <h2
    v-bind:id="identifier !== null ? identifier : false"
    class="mt-8 pl-3"
  >
    <slot></slot>
  </h2>
</template>

<script>
export default {
  name: 'BasePageGroupDivider',
  props: {
    identifier: {
      type: String,
      required: false,
      default: null,
    },
  },
};
</script>

<style scoped>

</style>
