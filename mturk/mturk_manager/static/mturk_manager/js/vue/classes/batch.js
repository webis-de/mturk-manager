import _ from 'lodash';
import Vue from 'vue';
import moment from "moment";

export default class Batch
{
	constructor(data={}) 
	{
		this.id = data.id;
		this.name = data.name;
		this.id_project = data.id_project;
		this.use_sandbox = data.use_sandbox;
		// this.object_hits = {};
		this.settings_batch = data.settings_batch;
		this.count_hits = data.count_hits;
		this.datetime_creation = moment(data.datetime_creation);
		this.count_assignments_available= data.count_assignments_available;
		this.count_assignments_total= data.count_assignments_total;
		this.count_assignments_approved= data.count_assignments_approved;
		this.count_assignments_rejected= data.count_assignments_rejected;
		this.costs_max = data.costs_max;
		this.costs_so_far = data.costs_so_far;
		// this._count_assignments_total = null;
		// this._count_assignments_available = null;
		// this._progress = null;
		// this._datetime_creation = null;
	}

    get progress() {
    	// if(this._progress != null) return this._progress;
// 
    	const progress = (this.count_assignments_available / this.count_assignments_total) * 100.0;
        // console.log('EXECUTED1')

    	// this._progress = progress;
        return (this.count_assignments_available / this.count_assignments_total) * 100.0;
    }
	//
    // get datetime_creation() {
    // 	// if(this._datetime_creation != null) return this._datetime_creation;
    //
    // 	if(_.size(this.object_hits) > 0)
    // 	{
    // 		return this.object_hits[_.keys(this.object_hits)[0]].datetime_creation;
    // 		// this._datetime_creation = this.object_hits[_.keys(this.object_hits)[0]].datetime_creation;
    // 		// return this._datetime_creation;
    // 	} else {
    // 		return undefined;
    // 	}
    // }
}