import { EntityInterface } from '@/modules/app/entity/entity.types';
import { ID } from '@/modules/app/types';
import Project from '@/classes/project';

export interface SettingsBatchInterface extends EntityInterface {
  name: string;
  title: string | null;
  description: string | null;
  reward: number;
  // TODO change type to keywords
  keywords: string[];
  duration: number;
  lifetime: number;
  countAssignments: number;
  countAssignmentsMaxPerWorker: number | null;
  blockWorkers: boolean;
  hasContentAdult: boolean;
  templateWorker: ID | null;
  project: Project;
  qualificationAssignmentsApproved: number | null;
  qualificationHitsApproved: number | null;
  qualificationLocale: string | null;
}
