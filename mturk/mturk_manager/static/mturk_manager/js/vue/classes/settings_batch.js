import _ from 'lodash';

export default class Settings_Batch 
{
	constructor(data=undefined) 
	{
		this.id = data != undefined ? data.id : undefined;
		this.name = data != undefined ? data.name : undefined;

        this.title = data != undefined ? data.title : undefined;
        this.description = data != undefined ? data.description : undefined;
        this.reward = data != undefined ? data.reward : undefined;
        this.keywords = data != undefined ? JSON.parse(JSON.stringify(data.keywords)) : [];
        this.count_assignments = data != undefined ? data.count_assignments : undefined;
        this.count_assignments_max_per_worker = data != undefined ? data.count_assignments_max_per_worker : undefined;
        this.lifetime = data != undefined ? data.lifetime : undefined;
        this.duration = data != undefined ? data.duration : undefined;
        this.block_workers = data != undefined ? data.block_workers : false;
        this.template = data != undefined ? data.template : undefined;
        
        this.has_content_adult = data != undefined ? data.has_content_adult : false;
        this.qualification_assignments_approved = data != undefined ? data.qualification_assignments_approved : undefined;
        this.qualification_hits_approved = data != undefined ? data.qualification_hits_approved : undefined;
        this.qualification_locale = data != undefined ? JSON.parse(JSON.stringify(data.qualification_locale)) : [];
	}

	get_changes(settings_batch) {
		const object = {};
		for(const key in this)
		{
			if(settings_batch[key] != undefined)
			{
				if(this[key] != settings_batch[key])
				{
					// if(key == 'keywords')
					// {
					// 	const keywords_processed = [];
					// 	for(let keyword of settings_batch[key])
					// 	{
					// 		if(typeof(keyword) == 'string')
					// 		{
					// 			keyword = {'text': keyword}
					// 		}

					// 		keywords_processed.push(keyword)
					// 	}
					// 	object[key] = keywords_processed;
					// } else if(key == 'qualification_assignments_approved' || key == 'qualification_hits_approved') {
					// 	settings_batch[key].trim() == '' ? object[key] = null : object[key] = settings_batch[key];
					// } else if(key == 'qualification_locale') {
					// 	object[key] = JSON.stringify(settings_batch[key]);
					// } else {
						// if(typeof(settings_batch[key]) == 'object')
						// {
						// } else {
						// 	if(key == 'assignments_max') 
						// 	{
						// 		object['count_assignments'] = settings_batch[key];
						// 	} else if(key == 'template') {
						// 		object['fk_template_main'] = settings_batch[key];
						// 	} else {
						// 		object[key] = settings_batch[key];
						// 	}
						// }
					// }
						if(typeof(settings_batch[key]) == 'object')
						{
							if(
								_.differenceBy(settings_batch[key], this[key], (value) => value['text'].toLowerCase()).length > 0 ||
								_.differenceBy(this[key], settings_batch[key], (value) => value['text'].toLowerCase()).length > 0
							) {
								object[key] = settings_batch[key];
							}

						} else {
							object[key] = settings_batch[key];
						}
				}
			}
		}

		return object;
	}
}