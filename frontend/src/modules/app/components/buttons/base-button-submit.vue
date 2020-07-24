<template>
  <v-btn
    type="submit"
    color="primary"
    v-bind:disabled="disabled"
    class="ml-7"
    v-on:click="$emit('click')"
  >
    <template v-if="$vuetify.breakpoint.smAndDown === true">
      <v-icon>
        fas fa-save
      </v-icon>
    </template>
    <template v-else>
      {{ label }}
    </template>
  </v-btn>
</template>

<script>
export default {
  name: 'BaseButtonSubmit',
  props: {
    label: {
      required: false,
      type: String,
      default() {
        return 'Submit';
      },
    },
    disabled: {
      required: false,
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>

</style>
