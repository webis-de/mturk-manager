import _ from 'lodash';

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
