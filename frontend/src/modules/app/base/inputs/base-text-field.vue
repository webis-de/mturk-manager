<template>
  <div>
    <v-text-field
      v-bind:value="value"
      v-bind="optionsMerged"
      v-bind:error-messages="errorsComputed"
      v-on:input="input"
    />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from '@vue/composition-api';
import { ErrorObject } from '@vuelidate/core';
import { getValidator, toNumber } from '@/modules/app/helpers';

export default defineComponent({
  name: 'BaseTextField',
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
    const hasValidationInfo = computed(() => props.validation !== undefined);

    const isRequired = computed(() => {
      if (hasValidationInfo.value) {
        return props.validation.required !== undefined;
      }
      return false;
    });

    const errorsComputed = computed(() => (hasValidationInfo.value ? props.validation.$errors.map(
      (error: ErrorObject) => error.$message,
    ) : []));

    const labelInternal = computed(() => {
      let { label } = props.options;

      if (label === undefined) {
        throw Error('Option \'label\' is missing');
      }

      if (isRequired.value) {
        label += ' (required)';
      }
      return label;
    });

    return {
      hasValidationInfo,
      isRequired,
      errorsComputed,
      optionsMerged: computed(() => ({
        ...props.options,
        label: labelInternal.value,
      })),
      input(value: string) {
        let valuePassed: string | number = value;
        if (props.options.type === 'number') {
          valuePassed = toNumber(valuePassed);
        }
        emit('input', valuePassed);
        props.validation.$touch();
      },
    };
  },
});
</script>

<style scoped>

</style>
