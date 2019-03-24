<template>
  <v-menu
    offset-y
    offset-x
    v-bind:close-on-content-click="false"
  >
    <v-btn
      icon
      small
      slot="activator"
    >
      <v-icon>help</v-icon>
    </v-btn>
    <v-card>
      <v-card-text>
        <slot></slot>
      </v-card-text>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  name: 'BaseHelp',
};
</script>

<style scoped>
.v-btn {
  padding: 0;
  margin: 0;
}
</style>
