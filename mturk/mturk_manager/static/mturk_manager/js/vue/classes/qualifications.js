export class Qualification {
	constructor(data) {
		this.id = data.QualificationTypeId;
		// this.created_at = new Date(data.CreationTime);
		this.description = data.Description;
		this.is_requestable = data.IsRequestable;
		this.name = data.Name;
		this.status = data.QualificationTypeStatus;
	}

	get_as_formdata() {
		const form_data = new FormData();
		form_data.set('id', this.id);
		form_data.set('created_at', this.created_at);
		form_data.set('description', this.description);
		form_data.set('is_requestable', this.is_requestable);
		form_data.set('name', this.name);
		form_data.set('status', this.status);

		return form_data;
		return {
			id: this.id,
			created_at: this.created_at,
			description: this.description,
			is_requestable: this.is_requestable,
			name: this.name,
			status: this.status,
		};
	}
}