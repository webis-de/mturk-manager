import _ from 'lodash';

export class Qualification {
  constructor(data = {}) {
    this.id_mturk = data.id_mturk;
    this.created_at = data.created_at != undefined ? new Date(data.created_at) : undefined;
    this.name_mturk = data.name_mturk;
    this.description_mturk = data.description_mturk;
    this.name_database = data.name_database;
    this.description_database = data.description_database;
    this.is_requestable = data.is_requestable;
    // this.is_active = data.is_active != undefined ? data.is_active : false;
    this.is_auto_granted = data.is_auto_granted;
    this.keywords = data.keywords;
  }

  has_database_entry() {
    return this.name_database != undefined;
  }

  display_name() {
    return this.name_database == undefined
      ? this.name_mturk
      : this.name_database;
  }

  display_description() {
    return this.description_database == undefined
      ? this.description_mturk
      : this.description_database;
  }

  get_json() {
    return JSON.stringify({
      id_mturk: this.id_mturk,
      name: this.name_database,
      description: this.description_database,
    });
  }

  get_as_formdata(only_updateable_fields = false) {
    const form_data = new FormData();

    const set_updateable_fields = new Set([
      'name_database',
      'description_database',
      'description_mturk',
      // 'is_active',
    ]);
    console.log(set_updateable_fields);

    _.forOwn(this, (value, key) => {
      if (value != undefined) {
        if (only_updateable_fields == true) {
          if (!set_updateable_fields.has(key)) {
            return true;
          }
        }

        form_data.set(key, value);
      }
    });
    // form_data.set('keywords', 'something,else');
    // form_data.set('name_mturk', 'something,else');

    return form_data;
  }

  copy() {
    const result = {};

    _.forOwn(this, (value, key) => {
      result[key] = value;
    });

    return new Qualification(result);
  }
}
