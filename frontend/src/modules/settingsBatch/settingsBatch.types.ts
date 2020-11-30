import { EntityInterface } from '@/modules/app/entity/entity.types';
import Project from '@/classes/project';
import { TemplateWorker } from '@/modules/template/templateWorker.model';

export type Keyword = { text: string, id: string };

export interface SettingsBatchInterface extends EntityInterface {
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
}
