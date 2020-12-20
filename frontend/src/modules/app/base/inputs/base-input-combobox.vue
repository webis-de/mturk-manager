<template>
  <v-row no-gutters>
    <v-col>
      <v-combobox
        v-bind:value="value"
        v-bind="optionsMerged"
        v-bind:error-messages="baseInput.errorsComputed"

        v-bind:search-input="searchInput"

        v-on:update:search-input="updateSearchInput"
        v-on:input="baseInput.input"
      >
        <template
          v-if="options.multiple === true"
          v-slot:selection="data"
        >
          <v-chip
            v-bind:input-value="data.selected"
            close
            small
            v-on:click:close="removeItem(data.item)"
          >
            <strong>
              {{ data.item.text !== undefined ? data.item.text : data.item }}
            </strong>&nbsp;
          </v-chip>
        </template>
      </v-combobox>
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
      validator: getValidator({
        string: true, object: true, array: true, null: true,
      }),
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
        clearable: true,
        'hide-selected': true,
        counter: props.options.multiple === true,
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
      removeItem: (item) => {
        baseInput.input(props.value.filter((valueItem) => item !== valueItem));
      },
    };
  },
});
</script>

<style scoped>

</style>
