import { STATUS_BLOCK } from './enums.js';

export class Worker 
{
	constructor(data) 
	{
		this.id = data.id;
		// this.m_created_at = new Date(data.CreationTime);
		// this.m_description = data.Description;
		// this.m_is_requestable = data.IsRequestable;
		this.name = data.name;
		this.is_blocked = data.is_blocked;
		// this.m_status = data.QualificationTypeStatus;
	}

	get_block_status() 
	{
		switch(this.is_blocked)
		{
			case STATUS_BLOCK.NONE:
				return 'Not Blocked';
			case STATUS_BLOCK.SOFT:
				return 'Soft Blocked';
			case STATUS_BLOCK.HARD:
				return 'Hard Blocked';
		}
		return this.is_blocked
	}

	get_as_formdata() 
	{
		const form_data = new FormData();
		// form_data.set('id', this.m_id);
		// form_data.set('created_at', this.m_created_at);
		// form_data.set('description', this.m_description);
		// form_data.set('is_requestable', this.m_is_requestable);
		form_data.set('name', this.name);
		// form_data.set('status', this.m_status);

		return form_data;
		return {
			id: this.m_id,
			created_at: this.m_created_at,
			description: this.m_description,
			is_requestable: this.m_is_requestable,
			name: this.name,
			status: this.m_status,
		};
	}

	// get_description() {
	// 	return this.m_description;
	// } 
	// get_is_requestable() {
	// 	return this.m_is_requestable;
	// } 
	// get_status() {
	// 	return this.m_status;
	// } 
}