<template>
  <v-dialog
    v-model="dialog"
    fullscreen
  >
    <template v-slot:activator="{ on }">
      <v-btn
        color="primary"
        small
        v-on="on"
      >
        <v-icon>mdi-plus</v-icon> Add Template
      </v-btn>
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
              <base-button-submit v-bind:disabled="disabled" />
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
  },
  data() {
    return {
      dialog: false,
    };
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
