import _ from 'lodash';

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

		this._count_assignments_total = null;
		this._count_assignments_available = null;
		this._progress = null;
	}

	// get name() {
	// 	console.log('get name');
	// 	return this._name;
	// }

	// set name(val) {
	// 	// return val;
	// 	this._name = val;
	// }

    get count_assignments_total() {
    	if(this._count_assignments_total != null) return this._count_assignments_total;

    	const count_assignments_total = this.settings_batch.count_assignments * this.hits.length;
    	this._count_assignments_total = count_assignments_total;
        return count_assignments_total;
    }

    get count_assignments_available() {
    	if(this._count_assignments_available != null) return this._count_assignments_available;

        let count_assignments_available = 0;
        console.log('EXPENSIVE1')
        _.forEach(this.hits, (hit) => {
            count_assignments_available += hit.assignments.length;
        });

    	this._count_assignments_available = count_assignments_available;
        return count_assignments_available;
    }

    get progress() {
    	if(this._progress != null) return this._progress;

    	const progress = (this.count_assignments_available / this.count_assignments_total) * 100.0;
        console.log('EXECUTED1')

    	this._progress = progress;
        return (this.count_assignments_available / this.count_assignments_total) * 100.0;
    }
}