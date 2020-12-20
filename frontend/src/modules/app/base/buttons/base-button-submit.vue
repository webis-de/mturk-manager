<template>
  <v-btn
    text
    type="submit"
    v-bind:color="color"
    v-bind:disabled="disabled"
    v-bind:form="idForm"
    class="ml-7"
    v-on:click="$emit('click')"
  >
    <!--    <template v-if="$vuetify.breakpoint.smAndDown === true">-->
    <!--      <v-icon>-->
    <!--        fas fa-save-->
    <!--      </v-icon>-->
    <!--    </template>-->
    <!--    <template v-else>-->
    {{ label }}
    <!--    </template>-->
  </v-btn>
</template>

<script>
export default {
  name: 'BaseButtonSubmit',
  props: {
    label: {
      required: false,
      type: String,
      default: 'Submit',
    },
    disabled: {
      required: false,
      type: Boolean,
      default: false,
    },
    color: {
      required: false,
      type: String,
      default: 'primary',
    },
    idForm: {
      required: false,
      type: String,
      default: undefined,
    },
  },
};
</script>

<style scoped>

</style>
