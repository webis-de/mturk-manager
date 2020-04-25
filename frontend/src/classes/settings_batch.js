import _ from 'lodash';
import Template_Worker from './template_worker';

export default class Settings_Batch {
  constructor(data = { template: new Template_Worker() }) {
    this.id = data.id;
    this.name = data.name;

    this.title = data.title;
    this.description = data.description;
    this.reward = data.reward;
    this.keywords = data.keywords !== undefined ? JSON.parse(JSON.stringify(data.keywords)) : [];
    this.count_assignments = data.count_assignments;
    this.count_assignments_max_per_worker = data.count_assignments_max_per_worker;
    this.lifetime = data.lifetime;
    this.duration = data.duration;
    this.block_workers = data.block_workers;
    this.template = data.template;

    this.has_content_adult = data.has_content_adult !== undefined ? data.has_content_adult : false;
    this.qualification_assignments_approved = data.qualification_assignments_approved;
    this.qualification_hits_approved = data.qualification_hits_approved;
    this.qualification_locale = data.qualification_locale !== undefined
      ? JSON.parse(JSON.stringify(data.qualification_locale))
      : [];
  }

  get_changes(settings_batch) {
    const object = {};
    for (const key in this) {
      if (settings_batch[key] != undefined) {
        if (this[key] != settings_batch[key]) {
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
          if (typeof settings_batch[key] === 'object') {
            if (
              _.differenceBy(settings_batch[key], this[key], value => value.text.toLowerCase()).length > 0
              || _.differenceBy(this[key], settings_batch[key], value => value.text.toLowerCase()).length > 0
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
