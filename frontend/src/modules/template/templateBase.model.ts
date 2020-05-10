export class TemplateBase {
  id?: string;

  name: string;

  template: string;

  isActive: boolean;

  datetimeCreation?: Date;

  constructor({
    id,
    name = '',
    template = '',
    isActive = true,
    datetimeCreation,
  }: {
    id?: string;
    name?: string;
    template?: string;
    isActive?: boolean;
    datetimeCreation?: Date;
  } = {}) {
    this.id = id;
    this.name = name;
    this.template = template;
    this.isActive = isActive;
    this.datetimeCreation = datetimeCreation;
  }
}
