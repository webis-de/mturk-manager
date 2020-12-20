import { maxValue, minValue, required } from '@vuelidate/validators';
import { Ref, ref } from '@vue/composition-api';
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';
import useVuelidate from '@vuelidate/core';
import { ServiceSettingsBatch } from '@/modules/settingsBatch/settingsBatch.service';

export function useCreate({ emit }: { emit: (event: string, ...args: unknown[]) => void }): {
  settingsBatchNew: Ref<SettingsBatch>,
  reset: () => void,
  v: unknown,
  create: ({ close }: {close:() => void}) => Promise<void>,
} {
  const rules = {
    name: {
      required,
      // is_unique: foo(
      //   this.project_current.settings_batch,
      //   this.settingsBatch,
      // ),
    },
    title: {
      required,
    },
    description: {
      required,
    },
    reward: {
      required,
      minValue: minValue(0),
    },
    countAssignments: {
      required,
      minValue: minValue(1),
    },
    // countAssignmentsMaxPerWorker: {
    //   minValue: minValue(0),
    // },
    lifetime: {
      required,
      minValue: minValue(0),
    },
    duration: {
      required,
      minValue: minValue(30),
      maxValue: maxValue(31536000),
    },
    templateWorker: {
      required,
    },
    blockWorkers: {
      required,
    },
    keywords: { },
    hasContentAdult: { required },
    qualificationAssignmentsApproved: {
      minValue: minValue(0),
      maxValue: maxValue(100),
    },
    qualificationHitsitsApproved: {
      minValue: minValue(0),
    },
    qualificationLocale: {},
  };
  const settingsBatchNew = ref(new SettingsBatch());
  const v = useVuelidate(rules, settingsBatchNew);

  const reset = () => {
    settingsBatchNew.value = new SettingsBatch();
    v.value.$reset();
  };

  return {
    settingsBatchNew,
    reset,
    v,
    create: async ({ close }) => {
      const isValid = await v.value.$validate();

      if (isValid) {
        ServiceSettingsBatch.create({
          settingsBatch: settingsBatchNew.value,
        }).then(() => {
          close();
          emit('created');
          reset();
        });
      }
    },
  };
}
