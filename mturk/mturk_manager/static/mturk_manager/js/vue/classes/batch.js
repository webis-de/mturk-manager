export default class Batch
{
	constructor(data={}) 
	{
		this.id = data.id;
		this.name = data.name;
		this.id_project = data.id_project;
		this.use_sandbox = data.use_sandbox;
		this.hits = [];
		// this.hits = JSON.parse(JSON.stringify(data.hits));
		this.settings_batch = data.settings_batch;
	}
}