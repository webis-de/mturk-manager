import { computed, ComputedRef } from '@vue/composition-api';
import type { Entity } from '@/modules/app/entity/entity.model';

export function useModelWrapper({
  props,
  emit,
  name = 'modelValue',
  isEntity = false,
  entities = {},
}: {
  props: Record<string, Entity | Entity[]>;
  // TODO is the unknown required?
  // props: Record<string, Entity | Entity[] | unknown>;
  emit: (event: string, ...args: unknown[]) => void;
  name: string;
  isEntity?: boolean;
  entities?: Record<string, unknown>;
}): ComputedRef {
  return computed({
    get: () => {
      if (isEntity === true) {
        if (Array.isArray(props[name])) {
          return (props[name] as Entity[]).map((entity: Entity) => entity.id);
        }
        return (props[name] as Entity)?.id;
      }
      return props[name];
    },
    set: (value) => {
      if (isEntity === true) {
        if (Array.isArray(value)) {
          emit(
            `update:${name}`,
            value.map((val: string) => ({ id: val })),
          );
        } else {
          emit(`update:${name}`, entities[value as string]);
        }
      } else {
        emit(`update:${name}`, value);
      }
    },
  });
}

export function setDefaultIfNullOrUndefined<T>(value: T | undefined, defaultValue: T): T {
  if (value === undefined || value === null) {
    return defaultValue as T;
  }
  return value;
}
