import _ from 'lodash';

export default class Template_Worker {
  constructor(data = {}) {
    this.id = data.id;
    this.name = data.name;
    this.height_frame = data.height_frame != undefined ? data.height_frame : 800;
    this.template = data.template;
    this.template_assignment = data.template_assignment;
    this.template_hit = data.template_hit;
    this.template_global = data.template_global;
    this.dict_parameters = data.json_dict_parameters != undefined
      ? JSON.parse(data.json_dict_parameters)
      : {};
    this.count_parameters = Object.keys(this.dict_parameters).length;
  }

  get_changes(template_worker) {
    const object = {};
    for (const key in this) {
      // if(template_worker[key] != undefined)
      {
        if (this[key] != template_worker[key]) {
          if (typeof template_worker[key] === 'object') {
            if (
              _.differenceBy(template_worker[key], this[key], value => value.text.toLowerCase()).length > 0
              || _.differenceBy(this[key], template_worker[key], value => value.text.toLowerCase()).length > 0
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
