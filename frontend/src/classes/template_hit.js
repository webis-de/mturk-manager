import _ from 'lodash';

export default class Template_HIT {
  constructor(data = undefined) {
    this.id = data != undefined ? data.id : undefined;
    this.name = data != undefined ? data.name : undefined;
    this.template = data != undefined ? data.template : undefined;
  }

  update(data) {
    _.forEach(data, (value, key) => {
      this[key] = value;
    });
  }

  get_changes(template_hit) {
    const object = {};
    for (const key in this) {
      // if(template_hit[key] != undefined)
      {
        if (this[key] != template_hit[key]) {
          if (typeof template_hit[key] === 'object') {
            if (
              _.differenceBy(template_hit[key], this[key], value => value.text.toLowerCase()).length > 0
              || _.differenceBy(this[key], template_hit[key], value => value.text.toLowerCase()).length > 0
            ) {
              object[key] = template_hit[key];
            }
          } else {
            const value = template_hit[key];
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
