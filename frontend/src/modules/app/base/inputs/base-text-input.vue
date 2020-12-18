<template>
  <v-row
    no-gutters
    align="baseline"
  >
    <v-col>
      <v-text-field
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
import { getValidator, toNumber } from '@/modules/app/helpers';
import { useBaseInput } from '@/modules/app/base/inputs/base-input';

export default defineComponent({
  name: 'BaseTextInput',
  props: {
    value: {
      required: true,
      validator: getValidator({ number: true, string: true, null: true }),
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
  setup(props, { emit }) {
    const baseInput = useBaseInput<
        string | null,
        string | number | null
    >(
      props,
      emit,
      (value) => {
        if (props.options.type === 'number') {
          const valueParsed = toNumber(value);

          return typeof valueParsed !== 'number' ? null : valueParsed;
        }

        return value;
      },
    );

    return {
      baseInput,
      optionsMerged: computed(() => ({
        ...props.options,
        label: baseInput.label.value,
      })),
    };
  },
});
</script>

<style scoped>

</style>
