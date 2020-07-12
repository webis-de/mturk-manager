import gql from 'graphql-tag';

export const fragmentsSettingsBatch = {
  settingsBatch: gql`fragment settingsBatch on TypeSettingsBatch {
    id
    project {
      id
    }
    name
    title
    description
    blockWorkers
    countAssignments
    countAssignmentsMaxPerWorker
    duration
    hasContentAdult
    keywords {
      id
      text
    }
    lifetime
    qualificationAssignmentsApproved
    qualificationHitsApproved
    qualificationLocale
    reward
    templateWorker {
      id
    }
  }`,
};
