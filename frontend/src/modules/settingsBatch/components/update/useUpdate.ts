import { Ref, ref } from '@vue/composition-api';
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';
import useVuelidate from '@vuelidate/core';
import { ServiceSettingsBatch } from '@/modules/settingsBatch/settingsBatch.service';
import { cloneDeep } from 'lodash-es';

export function useUpdate({
  settingsBatch,
  emit,
}: {
  settingsBatch: SettingsBatch,
  emit: (event: string, ...args: unknown[]) => void
}): {
  settingsBatch: Ref<SettingsBatch>,
  reset: () => void,
  v: unknown,
  update: ({ close }: {close:() => void}) => Promise<void>,
} {
  const settingsBatchUpdated = ref(cloneDeep(settingsBatch));
  const v = useVuelidate(ServiceSettingsBatch.getRules(), settingsBatchUpdated);

  const reset = () => {
    settingsBatchUpdated.value = cloneDeep(settingsBatch);
    v.value.$reset();
  };

  return {
    settingsBatchUpdated,
    reset,
    v,
    create: async ({ close }) => {
      const isValid = await v.value.$validate();

      if (isValid) {
        ServiceSettingsBatch.update({
          settingsBatch: settingsBatchUpdated.value,
        }).then(() => {
          close();
          emit('created');
          reset();
        });
      }
    },
  };
}
