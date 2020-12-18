<template>
  <v-row
    no-gutters
  >
    <v-col>
      <base-number-input
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
import { formatDuration, getValidator } from '@/modules/app/helpers';
import BaseNumberInput from '@/modules/app/base/inputs/base-number-input.vue';

export default defineComponent({
  name: 'BaseDurationInput',
  components: { BaseNumberInput },
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
    const durationFormatted = computed(() => formatDuration(props.value));

    return {
      optionsMerged: computed(() => ({
        ...props.options,
        suffix: `s , in words: ${durationFormatted.value}`,
      })),
      durationFormatted,
    };
  },
});
</script>

<style scoped>

</style>
