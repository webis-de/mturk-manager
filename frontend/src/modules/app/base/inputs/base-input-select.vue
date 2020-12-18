<template>
  <v-row
    no-gutters
    align="baseline"
  >
    <v-col>
      <v-select
        v-bind:value="value"
        v-bind="optionsMerged"
        v-bind:error-messages="baseInput.errorsComputed"

        v-on:input="baseInput.input"
      />
    </v-col>
    <v-col class="shrink text-no-wrap text-body-1" />
  </v-row>
</template>

<script lang="ts">
import { computed, defineComponent } from '@vue/composition-api';
import { getValidator } from '@/modules/app/helpers';
import { useBaseInput } from '@/modules/app/base/inputs/base-input';

export default defineComponent({
  name: 'BaseInputSelect',
  props: {
    value: {
      required: true,
      validator: getValidator({ object: true, null: true }),
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
    searchInput: {
      required: false,
      type: String,
      default: undefined,
    },
  },
  setup(props, { emit }) {
    const baseInput = useBaseInput<
        Record<string, unknown> | undefined,
        Record<string, unknown> | null
    >(
      props,
      emit,
      (value) => (value === undefined ? null : value),
    );

    return {
      baseInput,
      optionsMerged: computed(() => ({
        'return-object': true,
        ...props.options,
        label: baseInput.label.value,
      })),
    };
  },
});
</script>

<style scoped>

</style>
