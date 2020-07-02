import { TemplateBase } from '@/modules/template/templateBase.model';

export class TemplateAssignment extends TemplateBase {
  get type() {
    return 'assignment';
  }
}
