import { ref, watch } from '@vue/composition-api';
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';
import { store } from '@/store/vuex';
import _ from 'lodash';
import { ServiceKeywords } from '@/services/keywords.service';

export function useCreateBatch(instance) {
  const idSettingsBatchSelected = ref<number>();
  const settingsBatchSelected = ref<SettingsBatch | undefined>();
  const settingsBatch = ref<SettingsBatch>(new SettingsBatch());

  ServiceKeywords.load();

  watch(idSettingsBatchSelected, () => {
    if (idSettingsBatchSelected.value === undefined) {
      settingsBatchSelected.value = undefined;
      // this.update_fields();
      instance.$v.$reset();
    } else {
      settingsBatchSelected.value = store.state.moduleSettingsBatch.settingsBatch[idSettingsBatchSelected.value];
      // this.update_fields();
      instance.$v.$touch();
    }

    if (settingsBatchSelected.value !== undefined) {
      settingsBatch.value = _.cloneDeep(settingsBatchSelected.value);
    } else {
      settingsBatch.value = new SettingsBatch();
    }
  });

  return {
    idSettingsBatchSelected,
    settingsBatchSelected,
    settingsBatch,
  };
}
