import { ID } from '@/modules/app/types';

export class MessageBase {
  id?: ID;

  project?: ID;

  projects: ID[];

  message: string;

  constructor({
    id,
    project,
    projects,
    message,
  }: {
    id?: ID;
    project?: ID;
    projects: ID[];
    message: string;
  }) {
    this.id = id;
    this.project = project;
    this.projects = projects;
    this.message = message;
  }

  extractBody() {
    return {
      id: this.id,
      project: this.project,
      projects: this.projects,
      message: this.message,
    };
  }

  // static prepareFromServerToStore(data: {}[]): {[key: string]: TemplateBase} {
  //   const templates: TemplateBase[] = data.map((item: {}) => this.parseFromServer(item));
  //
  //   return templates.reduce((obj, template) => {
  //     obj[template.id as string] = template;
  //     return obj;
  //   }, {} as { [key: string]: TemplateBase });
  // }
  //
  // static parseFromServer(item: {}): TemplateBase {
  //   item.project = item.project.id;
  //   return new this(item);
  // }

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
