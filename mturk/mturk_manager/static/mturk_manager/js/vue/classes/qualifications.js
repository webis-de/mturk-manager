import _ from 'lodash';

export class Qualification {
	constructor(data={}) {
		this.id_mturk = data.id_mturk;
		this.created_at = data.created_at != undefined ? new Date(data.created_at) : undefined;
		this.name_mturk = data.name_mturk;
		this.description_mturk = data.description_mturk;
		this.name_database = data.name_database;
		this.description_database = data.description_database;
		this.is_requestable = data.is_requestable;
		this.is_active = data.is_active;
		this.is_auto_granted = data.is_auto_granted;
		this.keywords = data.keywords;
	}

	has_database_entry() {
		return this.name_database != undefined;
	}

	display_name() {
		return this.name_database == undefined ? this.name_mturk: this.name_database;
	}

	display_description() {
		return this.description_database == undefined ? this.description_mturk: this.description_database;
	}

	get_as_formdata() {
		const form_data = new FormData();

		_.forOwn(this, function(value, key) {
			if(value != undefined) {
				form_data.set(key, value);
			}
		});
		// form_data.set('keywords', 'something,else');
		// form_data.set('name_mturk', 'something,else');

		return form_data;
	}
}