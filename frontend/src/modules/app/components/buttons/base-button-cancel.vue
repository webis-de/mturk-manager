<template>
  <v-btn
    text
    v-bind:icon="$vuetify.breakpoint.smAndDown === true"
    v-on:click="$emit('click')"
  >
    <template v-if="$vuetify.breakpoint.smAndDown === true">
      <v-icon>fas fa-times</v-icon>
    </template>
    <template v-else>
      {{ label }}
    </template>
  </v-btn>
</template>

<script>
export default {
  name: 'BaseButtonCancel',
  props: {
    label: {
      required: false,
      type: String,
      default() {
        return 'Cancel';
      },
    },
  },
};
</script>

<style scoped>

</style>
