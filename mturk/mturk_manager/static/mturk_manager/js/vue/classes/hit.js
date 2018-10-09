export default class HIT
{
	constructor(data={}) 
	{
		this.id = data.id;
		this.id_hit = data.id_hit;
		this.batch = data.batch;
		this.count_assignments_additional = data.count_assignments_additional;
		this.datetime_creation = data.datetime_creation;
		this.datetime_expiration = data.datetime_expiration;
		this.parameters = data.parameters;
	}
}