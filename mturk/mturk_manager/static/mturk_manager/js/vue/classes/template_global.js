import _ from "lodash";

export default class Template_Global {
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

  get_changes(template_global) {
    const object = {};
    for (const key in this) {
      // if(template_global[key] != undefined)
      {
        if (this[key] != template_global[key]) {
          if (typeof template_global[key] == "object") {
            if (
              _.differenceBy(template_global[key], this[key], value =>
                value["text"].toLowerCase()
              ).length > 0 ||
              _.differenceBy(this[key], template_global[key], value =>
                value["text"].toLowerCase()
              ).length > 0
            ) {
              object[key] = template_global[key];
            }
          } else {
            const value = template_global[key];
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
