import _ from 'lodash';
import Vue from 'vue';

export default class Batch
{
	constructor(data={}) 
	{
		this.id = data.id;
		this.name = data.name;
		this.id_project = data.id_project;
		this.use_sandbox = data.use_sandbox;
		this.object_hits = {};
		this.settings_batch = data.settings_batch;

		// this._count_assignments_total = null;
		// this._count_assignments_available = null;
		// this._progress = null;
		// this._datetime_creation = null;
	}

    get count_assignments_total() {
    	// if(this._count_assignments_total != null) return this._count_assignments_total;

    	const count_assignments_total = this.settings_batch.count_assignments * _.size(this.object_hits);
    	// this._count_assignments_total = count_assignments_total;
        return count_assignments_total;
    }

    get count_assignments_available() {
    	// if(this._count_assignments_available != null) return this._count_assignments_available;

        let count_assignments_available = 0;
        // console.log('EXPENSIVE1')
        _.forEach(this.object_hits, (hit) => {
            count_assignments_available += _.size(hit.object_assignments);
        });

    	// this._count_assignments_available = count_assignments_available;
        return count_assignments_available;
    }

    get progress() {
    	// if(this._progress != null) return this._progress;
// 
    	const progress = (this.count_assignments_available / this.count_assignments_total) * 100.0;
        // console.log('EXECUTED1')

    	// this._progress = progress;
        return (this.count_assignments_available / this.count_assignments_total) * 100.0;
    }

    get datetime_creation() {
    	// if(this._datetime_creation != null) return this._datetime_creation;
    	
    	if(_.size(this.object_hits) > 0)
    	{
    		return this.object_hits[_.keys(this.object_hits)[0]].datetime_creation;
    		// this._datetime_creation = this.object_hits[_.keys(this.object_hits)[0]].datetime_creation;
    		// return this._datetime_creation;
    	} else {
    		return undefined;
    	}
    }
}