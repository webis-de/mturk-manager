export default class Assignment
{
	constructor(data={}) 
	{
		this.id = data.id;
		this.id_assignment = data.id_assignment;
		this.answer = data.answer;
		this.worker = data.worker;
		this.hit = data.hit;
		this.status_external = data.status_external;
		this.status_internal = data.status_internal;
		this.datetime_creation = new Date(data.datetime_update);
	}
}