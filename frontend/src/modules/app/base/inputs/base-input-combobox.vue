<template>
  <v-row no-gutters>
    <v-col>
      <v-combobox
        v-bind:value="value"
        v-bind="optionsMerged"
        v-bind:error-messages="baseInput.errorsComputed"

        v-bind:search-input="searchInput"

        dense
        no-filter

        v-on:update:search-input="updateSearchInput"
        v-on:input="baseInput.input"
      />
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { computed, defineComponent } from '@vue/composition-api';
import { getValidator } from '@/modules/app/helpers';
import { useBaseInput } from '@/modules/app/base/inputs/base-input';

export default defineComponent({
  name: 'BaseInputCombobox',
  props: {
    value: {
      required: true,
      validator: getValidator({ string: true, object: true, null: true }),
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
        Record<string, unknown> | string | undefined,
        Record<string, unknown> | string | null
    >(
      props,
      emit,
      (value) => (value === undefined ? null : value),
    );

    return {
      baseInput,
      optionsMerged: computed(() => ({
        ...props.options,
        label: baseInput.label.value,
      })),
      updateSearchInput: (value) => {
        let valuePassed = value;

        if (valuePassed === undefined) {
          valuePassed = null;
        }

        emit('update:search-input', valuePassed);
      },
    };
  },
});
</script>

<style scoped>

</style>
