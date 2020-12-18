import { computed, ComputedRef } from '@vue/composition-api';
import { ErrorObject } from '@vuelidate/core';

export function useBaseInput<I, E>(
  props: {validation: unknown, options: unknown},
  emit: (event: string, ...args: unknown[]) => void,
  parseValue: (value: I) => E = (value) => value as unknown as E,
): {
    label: ComputedRef<string>,
    errorsComputed: ComputedRef<string[]>,
    input: (value: I) => void
  } {
  const hasValidationInfo = computed(() => props.validation !== undefined);

  const isRequired = computed(() => {
    if (hasValidationInfo.value) {
      return props.validation.required !== undefined;
    }
    return false;
  });

  const errorsComputed = computed<string[]>(() => (hasValidationInfo.value ? props.validation.$errors.map(
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

  const input = (value: I) => {
    const valueParsed: E = parseValue(value);

    emit('input', valueParsed);

    if (hasValidationInfo.value) {
      props.validation.$touch();
    }
  };

  return {
    label: labelInternal,
    errorsComputed,
    input,
  };
}
