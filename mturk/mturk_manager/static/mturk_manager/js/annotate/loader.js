import _ from 'lodash';
import { normalize_answer } from './helpers';

export default class Loader
{
	constructor()
	{
		this.context = JSON.parse($('#context').html());
		this.project = {};
		this.message_reject_default = '';
		this.object_assignments = {};
		this.object_hits = {};
		this.object_batches = {};
		this.object_workers = {};
		this.set_ids_worker = new Set();
		this.array_messages_reject = [];

		this.object_assignments_selected = {};
		console.log(this.context)

		this.init()
	}

	async sync_data()
	{
		await this.load_project();
		await this.load_assignments();
    	await this.load_hits();
		await this.load_batches()
		await this.load_workers();
		await this.load_messages_reject();
	}

	async load_messages_reject() {
		const url = this.context.url_api_messages_reject;

		const result = await $.ajax({
	        url: url,
	        method: 'GET',
	        contentType: 'application/json',
	        headers: {
	            Authorization: 'Token ' + this.context.token_instance,
	            "Content-Type": 'application/json',
	        },
	    });

		this.array_messages_reject = _.orderBy(result, 'usage_count', 'desc')
	}

	async load_project() {
		const url = this.context.url_api_project;

		const result = await $.ajax({
	        url: url,
	        method: 'GET',
	        data: JSON.stringify(_.toArray(this.set_ids_worker)),
	        contentType: 'application/json',
	        headers: {
	            Authorization: 'Token ' + this.context.token_instance,
	            "Content-Type": 'application/json',
	        },
	    });

		this.project = result;
		if(this.project.message_reject_default != undefined)
		{
			this.message_reject_default = this.project.message_reject_default.message			
		}
	}

	async load_assignments()
	{
		let url = this.context.url_api_assignments;
		url += '?list_ids=['+this.context.list_ids.join(',')+']';

		const result = await $.ajax({
	        url: url,
	        method: 'GET',
	        contentType: 'application/json',
	        headers: {
	            Authorization: 'Token ' + this.context.token_instance,
	            "Content-Type": 'application/json',
	        },
	    });

		_.forEach(result, (assignment) => {
			this.set_ids_worker.add(assignment.worker);
			assignment.answer = normalize_answer(assignment.answer);
    		this.object_assignments[assignment.id] = assignment;
		});

	}

	async load_hits()
	{
		const set_ids_hit = new Set();
		_.forEach(this.object_assignments, (assignment) => {
			set_ids_hit.add(assignment.hit);
		});

		let url = this.context.url_api_hits;
		url += '?list_ids=['+_.toArray(set_ids_hit).join(',')+']';

		const result = await $.ajax({
	        url: url,
	        method: 'GET',
	        contentType: 'application/json',
	        headers: {
	            Authorization: 'Token ' + this.context.token_instance,
	            'Content-Type': 'application/json',
	        },
	    });

		_.forEach(result, (hit) =>  {
			hit.parameters = JSON.parse(hit.parameters);
    		this.object_hits[hit.id] = hit;
		});

		_.forEach(this.object_assignments, (assignment) => {
			const hit = this.object_hits[assignment.hit];
			assignment.hit = hit;

			if(hit.assignments == undefined)
			{
				hit.assignments = [assignment];
			} else {
				hit.assignments.push(assignment);
			}
		});
	}

	async load_batches()
	{
		const set_ids_batch = new Set();
		_.forEach(this.object_hits, (hit) => {
			set_ids_batch.add(hit.batch);
		});

		let url = this.context.url_api_batches;
		url += '?list_ids=['+_.toArray(set_ids_batch).join(',')+']';

		const result = await $.ajax({
	        url: url,
	        method: 'GET',
	        contentType: 'application/json',
	        headers: {
	            Authorization: 'Token ' + this.context.token_instance,
	            'Content-Type': 'application/json',
	        },
	    });

		_.forEach(result, (batch) => {
    		this.object_batches[batch.id] = batch;
		});

		_.forEach(this.object_hits, (hit) => {
			const batch = this.object_batches[hit.batch];
			hit.batch = batch;

			if(batch.hits == undefined)
			{
				batch.hits = [hit];
			} else {
				batch.hits.push(hit);
			}
		});
	}

	async load_workers() {
		const url = this.context.url_api_workers;

		const result = await $.ajax({
	        url: url,
	        method: 'PATCH',
	        data: JSON.stringify(_.toArray(this.set_ids_worker)),
	        contentType: 'application/json',
	        headers: {
	            Authorization: 'Token ' + this.context.token_instance,
	            "Content-Type": 'application/json',
	        },
	    });

		_.forEach(result, (worker) => {
    		this.object_workers[worker.id] = worker;
		});

		_.forEach(this.object_assignments, (assignment) => {
			assignment.worker = this.object_workers[assignment.worker];
		});
	}

	init() {
		_.forEach(this.context, (value, key) => {
			if(key.startsWith('url_'))
			{
				this.context[key] = value.replace('PLACEHOLDER_SLUG_PROJECT', this.context.slug_project);
			}
			// console.log(key)
			// console.log(property)
		})
	}
}