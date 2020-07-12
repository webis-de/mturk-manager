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
// export const queryCreateSettingsBatch = gql`mutation createSettingsBatch(settingsBatch: InputSettingsBatch!) {
//     createSettingsBatch(idSettingsBatch: settingsBatch) {
//         template {
//             ...settingsBatch
//         }
//     }
// }
// ${fragmentsSettingsBatch.settingsBatch}
// `;
// /**
//  * Update
//  */
// export const queryUpdateSettingsBatch = gql`mutation updateSettingsBatch(settingsBatch: InputSettingsBatch!) {
//     updateSettingsBatch(idSettingsBatch: settingsBatch) {
//         template {
//             ...settingsBatch
//         }
//     }
// }
// ${fragmentsSettingsBatch.settingsBatch}
// `;
// /**
//  * Delete
//  */
// export const queryDeleteSettingsBatch = gql`mutation deleteSettingsBatch($id: ID!) {
//     deleteSettingsBatch(idSettingsBatch: $id) {
//         idTemplate
//     }
// }`;
