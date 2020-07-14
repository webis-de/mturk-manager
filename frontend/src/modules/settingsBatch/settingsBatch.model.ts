import { ID } from '@/modules/app/types';
import cloneDeep from 'lodash-es/cloneDeep';

export class SettingsBatch {
  id?: string;

  name: string;

  title?: string;

  description?: string;

  reward: number;

  // TODO change type to keywords
  keywords: string[];

  duration: number;

  lifetime: number;

  countAssignments: number;

  countAssignmentsMaxPerWorker?: number;

  blockWorkers: boolean;

  hasContentAdult: boolean;

  datetimeCreation?: Date;

  templateWorker?: ID;

  project: ID;

  projectDefault: ID;

  qualificationAssignmentsApproved?: number;

  qualificationHitsApproved?: number;

  qualificationLocale?: string;

  constructor({
    id,
    name,
    title,
    description,
    reward,
    keywords = [],
    duration,
    lifetime,
    countAssignments,
    countAssignmentsMaxPerWorker,
    blockWorkers = false,
    hasContentAdult,
    datetimeCreation,
    templateWorker,
    project,
    projectDefault,
    qualificationAssignmentsApproved,
    qualificationHitsApproved,
    qualificationLocale,
  }: {
    id?: string;
    name: string;
    title?: string;
    description?: string;
    reward: number;
    keywords: string[];
    duration: number;
    lifetime: number;
    countAssignments: number;
    countAssignmentsMaxPerWorker?: number;
    blockWorkers: boolean;
    hasContentAdult: boolean;
    datetimeCreation?: Date;
    templateWorker?: ID;
    project: ID;
    projectDefault: ID;
    qualificationAssignmentsApproved?: number;
    qualificationHitsApproved?: number;
    qualificationLocale?: string;
  } = {}) {
    this.id = id;
    this.name = name;
    this.title = title;
    this.description = description;
    this.reward = reward;
    this.keywords = keywords;
    this.duration = duration;
    this.lifetime = lifetime;
    this.countAssignments = countAssignments;
    this.countAssignmentsMaxPerWorker = countAssignmentsMaxPerWorker;
    this.blockWorkers = blockWorkers;
    this.hasContentAdult = hasContentAdult;
    this.datetimeCreation = datetimeCreation;
    this.templateWorker = templateWorker;
    this.project = project;
    this.projectDefault = projectDefault;
    this.qualificationAssignmentsApproved = qualificationAssignmentsApproved;
    this.qualificationHitsApproved = qualificationHitsApproved;
    this.qualificationLocale = qualificationLocale;
  }

  extractBody() {
    return {
      id: this.id,
      project: this.project,
      name: this.name,
      templateWorker: this.templateWorker,
      datetimeCreation: this.datetimeCreation,
      title: this.title,
      description: this.description,
      reward: this.reward,
      keywords: this.keywords,
      duration: this.duration,
      lifetime: this.lifetime,
      countAssignments: this.countAssignments,
      countAssignmentsMaxPerWorker: this.countAssignmentsMaxPerWorker,
      blockWorkers: this.blockWorkers,
      hasContentAdult: this.hasContentAdult,
      projectDefault: this.projectDefault,
      qualificationAssignmentsApproved: this.qualificationAssignmentsApproved,
      qualificationHitsApproved: this.qualificationHitsApproved,
      qualificationLocale: this.qualificationLocale,
    };
  }

  static prepareFromServerToStore(data: {}[]): {[key: string]: SettingsBatch} {
    const settingsBatches: SettingsBatch[] = cloneDeep(data).map((item: {}) => this.parseFromServer(item));

    return settingsBatches.reduce((obj, settingsBatch) => {
      obj[settingsBatch.id as string] = settingsBatch;
      return obj;
    }, {} as { [key: string]: SettingsBatch });
  }

  static parseFromServer(item: {}): SettingsBatch {
    item.project = item.project.id;

    if (item.templateWorker !== null) {
      item.templateWorker = item.templateWorker.id;
    }

    item.keywords = item.keywords.map(keyword => ({id: keyword.id, text: keyword.text}));

    return new this(item);
  }

  // getChanges(template) {
  //   const object = {};
  //   for (const key in this) {
  //     // if(template_assignment[key] != undefined)
  //     {
  //       if (this[key] != template[key]) {
  //         if (typeof template[key] === 'object') {
  //           if (
  //             _.differenceBy(template[key], this[key], value => value.text.toLowerCase()).length > 0
  //             || _.differenceBy(this[key], template[key], value => value.text.toLowerCase()).length > 0
  //           ) {
  //             object[key] = template[key];
  //           }
  //         } else {
  //           const value = template[key];
  //           if (value == undefined) {
  //             object[key] = null;
  //           } else {
  //             object[key] = value;
  //           }
  //         }
  //       }
  //     }
  //   }
  //
  //   return object;
  // }
}
