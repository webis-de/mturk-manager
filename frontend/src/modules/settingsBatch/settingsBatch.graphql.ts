import gql from 'graphql-tag';
import { fragmentsSettingsBatch } from '@/modules/settingsBatch/settingsBatch.fragment';

export const querySettingsBatch = gql`query settingsBatch($project: ID!) {
    settingsBatch(project: $project) {
        ...settingsBatch
    }
}
${fragmentsSettingsBatch.settingsBatch}
`;
/**
 * Create
 */
export const queryCreateSettingsBatch = gql`mutation createSettingsBatch($settingsBatch: InputSettingsBatch!) {
    createSettingsBatch(settingsBatch: $settingsBatch) {
        settingsBatch {
            ...settingsBatch
        }
    }
}
${fragmentsSettingsBatch.settingsBatch}
`;
/**
 * Update
 */
export const queryUpdateSettingsBatch = gql`mutation updateSettingsBatch($settingsBatch: InputSettingsBatch!) {
    updateSettingsBatch(settingsBatch: $settingsBatch) {
         settingsBatch {
            ...settingsBatch
        }
    }
}
${fragmentsSettingsBatch.settingsBatch}
`;
/**
 * Delete
 */
export const queryDeleteSettingsBatch = gql`mutation deleteSettingsBatch($id: ID!) {
    deleteSettingsBatch(idSettingsBatch: $id) {
        idSettingsBatch
    }
}`;
