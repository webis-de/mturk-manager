<template>
  <v-dialog
    v-model="dialog"
    v-bind:fullscreen="fullscreen"
    v-bind:max-width="maxWidth"
  >
    <template v-slot:activator="{ on }">
      <slot
        name="activator"
        v-bind="{ on }"
      >
        <v-btn
          color="primary"
          small
          v-on="on"
        >
          <slot name="activator-content">
            <v-icon>{{ activatorIcon }}</v-icon> {{ activatorLabel }}
          </slot>
        </v-btn>
      </slot>
    </template>

    <v-card>
      <form
        v-bind:style="stylesForm"
        class="d-flex flex-column"
        v-on:submit.prevent="$emit('submit', { close: cancel })"
      >
        <v-card-title>
          <span class="headline">{{ title }}</span>
          <v-spacer />
          <v-btn
            icon
            v-on:click="cancel"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="flex-grow-1">
          <slot name="default"></slot>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <slot name="actions">
            <slot name="actions-cancel">
              <base-button-cancel
                v-on:click="cancel"
              />
            </slot>
            <slot name="actions-submit">
              <base-button-submit
                v-bind:disabled="disabled"
                v-bind:color="colorButtonSubmit"
                v-bind:label="labelButtonSubmit"
              />
            </slot>
          </slot>
        </v-card-actions>
      </form>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api';
import BaseButtonCancel from './buttons/base-button-cancel.vue';
import BaseButtonSubmit from './buttons/base-button-submit.vue';

export default defineComponent({
  name: 'BaseDialog',
  components: { BaseButtonSubmit, BaseButtonCancel },
  props: {
    title: {
      required: true,
      type: String,
    },
    disabled: {
      required: false,
      type: Boolean,
      default: false,
    },
    small: {
      required: false,
      type: Boolean,
      default: false,
    },
    colorButtonSubmit: {
      required: false,
      type: String,
      default: undefined,
    },
    labelButtonSubmit: {
      required: false,
      type: String,
      default: undefined,
    },
    activatorLabel: {
      required: false,
      type: String,
      default: 'Open',
    },
    activatorIcon: {
      required: false,
      type: String,
      default: '',
    },
  },
  data() {
    return {
      dialog: false,
    };
  },
  computed: {
    stylesForm() {
      if (!this.fullscreen) return {};

      return {
        position: 'absolute',
        height: '100%',
        width: '100%',
      };
    },
    fullscreen() {
      return !this.small;
    },
    maxWidth() {
      return this.small && this.$vuetify.breakpoint.lgAndUp ? '50%' : undefined;
    },
  },
  methods: {
    cancel() {
      this.dialog = false;
      this.$emit('cancel');
    },
  },
});
</script>

<style scoped>

</style>
