export default class Batch 
{
	constructor(data={}) 
	{
		this.id = data.id;
		this.name = data.name;
		this.count_assignments = data.count_assignments;
		this.hits = data.hits;
	}
}