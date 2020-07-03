import { TemplateBase } from '@/modules/template/templateBase.model';
import { ID } from '@/modules/app/types';

export class TemplateWorker extends TemplateBase {
  heightFrame: number;

  dictParameters: {};

  templateAssignment: ID | null;

  templateHIT: ID | null;

  templateGlobal: ID | null;

  templateOriginal: ID | null;

  constructor({
    heightFrame = 800,
    jsonDictParameters = '{}',
    templateAssignment = null,
    templateHIT = null,
    templateGlobal = null,
    templateOriginal = null,
    ...data
  }: {
    id?: string;
    name?: string;
    template?: string;
    isActive?: boolean;
    datetimeCreation?: Date;
    heightFrame?: number;
    jsonDictParameters?: string;
    templateAssignment?: ID | null;
    templateHIT?: ID | null;
    templateGlobal?: ID | null;
    templateOriginal?: ID | null;
  } = {}) {
    super(data);

    this.heightFrame = heightFrame;
    this.dictParameters = JSON.parse(jsonDictParameters);
    this.templateAssignment = templateAssignment;
    this.templateHIT = templateHIT;
    this.templateGlobal = templateGlobal;
    this.templateOriginal = templateOriginal;
  }

  get type() {
    return 'worker';
  }

  extractBody() {
    return {
      ...super.extractBody(),
      heightFrame: this.heightFrame,
      jsonDictParameters: JSON.stringify(this.dictParameters),
      templateAssignment: this.templateAssignment,
      templateHit: this.templateHIT,
      templateGlobal: this.templateGlobal,
      templateOriginal: this.templateOriginal,
    };
  }

  static parseFromServer(item: {}): TemplateBase {
    item.templateAssignment = item.templateAssignment !== null ? item.templateAssignment.id : null;
    // note the renaming from Hit to HIT
    item.templateHIT = item.templateHit !== null ? item.templateHit.id : null;
    item.templateGlobal = item.templateGlobal !== null ? item.templateGlobal.id : null;

    return super.parseFromServer(item);
  }
}
