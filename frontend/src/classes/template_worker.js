import _ from 'lodash';

export class TemplateWorker {
  constructor(data = {}) {
    this.id = data.id;
    this.name = data.name;
    this.height_frame = data.height_frame != undefined ? data.height_frame : 800;
    this.template = data.template !== undefined ? data.template : '';
    this.template_assignment = _.cloneDeep(data.template_assignment);
    this.template_hit = _.cloneDeep(data.template_hit);
    this.template_global = _.cloneDeep(data.template_global);
    this.has_assignments = data.has_assignments;
    this.dict_parameters = data.json_dict_parameters != undefined
      ? JSON.parse(data.json_dict_parameters)
      : {};
    this.count_parameters = Object.keys(this.dict_parameters).length;
  }

  getChanges(template_worker) {
    const object = {};
    for (const key in this) {
      // if(template_worker[key] != undefined)
      {
        if (this[key] != template_worker[key]) {
          if (typeof template_worker[key] === 'object') {
            if (
              _.differenceBy(template_worker[key], this[key], (value) => value.text.toLowerCase()).length > 0
              || _.differenceBy(this[key], template_worker[key], (value) => value.text.toLowerCase()).length > 0
              || this[key] === null
              || template_worker[key] === null
            ) {
              object[key] = template_worker[key];
            }
          } else {
            const value = template_worker[key];
            if (value == undefined) {
              object[key] = null;
            } else {
              object[key] = value;
            }
          }
        }
      }
    }

    return object;
  }
}
