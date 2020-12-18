<template>
  <v-row no-gutters>
    <v-col>
      <base-text-input
        v-bind:value="value"
        v-bind:validation="validation"
        v-bind:options="optionsMerged"
        v-on:input="$emit('input', $event)"
      />
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { computed, defineComponent } from '@vue/composition-api';
import BaseTextInput from '@/modules/app/base/inputs/base-text-input.vue';
import { getValidator } from '@/modules/app/helpers';

export default defineComponent({
  name: 'BaseNumberInput',
  components: { BaseTextInput },
  props: {
    value: {
      required: true,
      validator: getValidator({ number: true, null: true }),
    },
    validation: {
      required: false,
      type: Object,
      default: undefined,
    },
    options: {
      required: false,
      type: Object,
      default: () => ({}),
    },
  },
  setup(props) {
    return {
      optionsMerged: computed(() => ({
        ...props.options,
        type: 'number',
      })),
    };
  },
});
</script>

<style scoped>

</style>
