import _ from "lodash";

export default class Template_Assignment {
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

  get_changes(template_assignment) {
    const object = {};
    for (const key in this) {
      // if(template_assignment[key] != undefined)
      {
        if (this[key] != template_assignment[key]) {
          if (typeof template_assignment[key] == "object") {
            if (
              _.differenceBy(template_assignment[key], this[key], value =>
                value["text"].toLowerCase()
              ).length > 0 ||
              _.differenceBy(this[key], template_assignment[key], value =>
                value["text"].toLowerCase()
              ).length > 0
            ) {
              object[key] = template_assignment[key];
            }
          } else {
            const value = template_assignment[key];
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
