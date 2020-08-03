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
          <v-icon>mdi-plus</v-icon> Add Template
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
          <slot name="content"></slot>
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

<script>
import BaseButtonCancel from './buttons/base-button-cancel';
import BaseButtonSave from './buttons/base-button-submit';
import BaseButtonSubmit from './buttons/base-button-submit';

export default {
  name: 'BaseDialog',
  components: { BaseButtonSubmit, BaseButtonSave, BaseButtonCancel },
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
  },
  data() {
    return {
      dialog: false,
    };
  },
  computed: {
    stylesForm() {
      if (this.fullscreen === false) return {};

      return {
        position: 'absolute',
        height: '100%',
        width: '100%',
      };
    },
    fullscreen() {
      return this.small === false;
    },
    maxWidth() {
      return this.small === true && this.$vuetify.breakpoint.lgAndUp ? '50%' : undefined;
    },
  },
  methods: {
    cancel() {
      this.dialog = false;
      this.$emit('cancel');
    },
  },
};
</script>

<style scoped>

</style>
