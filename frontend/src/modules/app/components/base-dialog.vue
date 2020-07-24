<template>
  <v-dialog
    v-model="dialog"
    v-bind:fullscreen="small === false"
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
      <form v-on:submit.prevent="$emit('submit', { close: cancel })">
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
        <v-card-text>
          <slot name="content"></slot>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <slot name="actions">
            <slot name="actions-cancel">
              <base-button-cancel
                v-on:click="cancel"
              />
              <!--              <v-btn-->
              <!--                text-->
              <!--                class="ml-0"-->
              <!--                color="înfo"-->
              <!--                v-on:click="-->
              <!--                "-->
              <!--              >-->
              <!--                Cancel-->
              <!--              </v-btn>-->
            </slot>
            <slot name="actions-submit">
              <base-button-submit
                v-bind:disabled="disabled"
                v-bind:color="colorButtonSubmit"
                v-bind:label="labelButtonSubmit"
              />
              <!--              <v-btn-->
              <!--                text-->
              <!--                class="ml-0"-->
              <!--                type=""-->
              <!--                color="primary"-->
              <!--                v-bind:disabled="$v.$invalid"-->
              <!--                v-on:click="create()"-->
              <!--              >-->
              <!--                Save-->
              <!--              </v-btn>-->
            </slot>
          </slot>
        </v-card-actions>
      </form>
    </v-card>
    </form>
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
