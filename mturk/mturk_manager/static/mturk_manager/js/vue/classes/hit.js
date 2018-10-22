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
		this.assignments = [];

		this._count_assignments_total = null;
		this._count_assignments_available = null;
		this._progress = null;
	}

    get count_assignments_total() {
    	if(this._count_assignments_total != null) return this._count_assignments_total;

    	const count_assignments_total = this.batch.settings_batch.count_assignments;
    	this._count_assignments_total = count_assignments_total;
        return count_assignments_total;
    }

    get count_assignments_available() {
    	if(this._count_assignments_available != null) return this._count_assignments_available;

    	const count_assignments_available = this.assignments.length;
    	this._count_assignments_available = count_assignments_available;
        return count_assignments_available;
    }

    get progress() {
    	if(this._progress != null) return this._progress;

    	const progress = (this.count_assignments_available / this.count_assignments_total) * 100.0;
    	this._progress = progress;
        return progress;
    }

}