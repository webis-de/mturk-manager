<template>
  <v-row no-gutters>
    <v-col
      style="margin-top: 4px"
    >
      <v-radio-group
        v-bind:value="value"
        v-bind="optionsMerged"
        v-bind:error-messages="baseInput.errorsComputed"

        v-on:change="baseInput.input"
      >
        <v-radio
          label="Yes"
          v-bind:value="true"
        />
        <v-radio
          label="No"
          v-bind:value="false"
        />
      </v-radio-group>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { computed, defineComponent } from '@vue/composition-api';
import { getValidator } from '@/modules/app/helpers';
import { useBaseInput } from '@/modules/app/base/inputs/base-input';

export default defineComponent({
  name: 'BaseInputBoolean',
  props: {
    value: {
      required: true,
      validator: getValidator({ boolean: true }),
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
    const baseInput = useBaseInput<boolean, boolean>(props, emit);

    return {
      baseInput,
      optionsMerged: computed(() => ({
        row: true,
        ...props.options,
        label: baseInput.label.value,
      })),
    };
  },
});
</script>

<style scoped>

</style>
