import { Optional } from '@/modules/app/types';
import { Entity } from '@/modules/app/entity/entity.model';
import type { Keyword, SettingsBatchInterface } from '@/modules/settingsBatch/settingsBatch.types';
import { setDefaultIfNullOrUndefined } from '@/modules/app/helpers';
import { store } from '@/store/vuex';
import Project from '@/classes/project';
import { TemplateWorker } from '@/modules/template/templateWorker.model';

export class SettingsBatch extends Entity implements SettingsBatchInterface {
  name: string;

  title: string | null;

  description: string | null;

  reward: number;

  keywords: Keyword[];

  duration: number;

  lifetime: number;

  countAssignments: number;

  countAssignmentsMaxPerWorker: number | null;

  blockWorkers: boolean;

  hasContentAdult: boolean;

  templateWorker: TemplateWorker | null;

  project: Project;

  qualificationAssignmentsApproved: number | null;

  qualificationHitsApproved: number | null;

  qualificationLocale: string | null;

  constructor(data: Optional<SettingsBatchInterface, 'project'> = { project: store.getters['moduleProjects/getProjectCurrent'] }) {
    super(data);

    this.name = setDefaultIfNullOrUndefined(data.name, '');
    this.title = setDefaultIfNullOrUndefined(data.title, null);
    this.description = setDefaultIfNullOrUndefined(data.description, null);
    this.reward = setDefaultIfNullOrUndefined(data.reward, 0);
    this.keywords = setDefaultIfNullOrUndefined(data.keywords, []);
    this.duration = setDefaultIfNullOrUndefined(data.duration, 0);
    this.lifetime = setDefaultIfNullOrUndefined(data.lifetime, 0);
    // TODO minimum 1?
    this.countAssignments = setDefaultIfNullOrUndefined(data.countAssignments, 0);
    this.countAssignmentsMaxPerWorker = setDefaultIfNullOrUndefined(data.countAssignmentsMaxPerWorker, null);
    this.blockWorkers = setDefaultIfNullOrUndefined(data.blockWorkers, false);
    this.hasContentAdult = setDefaultIfNullOrUndefined(data.hasContentAdult, false);
    this.templateWorker = setDefaultIfNullOrUndefined(data.templateWorker, null);
    this.project = data.project;
    this.qualificationAssignmentsApproved = setDefaultIfNullOrUndefined(data.qualificationAssignmentsApproved, null);
    this.qualificationHitsApproved = setDefaultIfNullOrUndefined(data.qualificationHitsApproved, null);
    this.qualificationLocale = setDefaultIfNullOrUndefined(data.qualificationLocale, null);
  }

  prepareForServer(): Record<string, unknown> {
    const data = super.prepareForServer();

    data.project = this.project === null ? null : this.project.id;
    data.name = this.name;
    data.templateWorker = this.templateWorker === null ? null : this.templateWorker.id;
    data.title = this.title;
    data.description = this.description;
    data.reward = this.reward;
    data.keywords = this.keywords;
    data.duration = this.duration;
    data.lifetime = this.lifetime;
    data.countAssignments = this.countAssignments;
    data.countAssignmentsMaxPerWorker = this.countAssignmentsMaxPerWorker;
    data.blockWorkers = this.blockWorkers;
    data.hasContentAdult = this.hasContentAdult;
    data.qualificationAssignmentsApproved = this.qualificationAssignmentsApproved;
    data.qualificationHitsApproved = this.qualificationHitsApproved;
    data.qualificationLocale = JSON.stringify(this.qualificationLocale);

    return data;
  }

  static async parseFromServer(data: SettingsBatchInterface): Promise<SettingsBatch> {
    const entity = (await super.parseFromServer(data)) as SettingsBatch;

    entity.project = store.getters['moduleProjects/getProjectCurrent'];

    if (entity.templateWorker !== null) {
      entity.templateWorker = store.state.moduleTemplates.templatesWorker[entity.templateWorker.id];
    }

    entity.keywords = entity.keywords.map((keyword) => ({ id: keyword.id, text: keyword.text }));

    entity.qualificationLocale = entity.qualificationLocale === null ? [] : JSON.parse(entity.qualificationLocale);

    return entity;
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
