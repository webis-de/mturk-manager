import _ from 'lodash';
import { TemplateWorker } from './template_worker';

export class SettingsBatch {
  constructor(data = { template: new TemplateWorker() }) {
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

  getChanges(settingsBatch) {
    const object = {};
    const keys = Object.keys(this);
    for (let i = 0; i < keys.length; i += 1) {
      const key = keys[i];
      if (settingsBatch[key] !== undefined) {
        if (this[key] !== settingsBatch[key]) {
          // if(key == 'keywords')
          // {
          // 	const keywords_processed = [];
          // 	for(let keyword of settingsBatch[key])
          // 	{
          // 		if(typeof(keyword) == 'string')
          // 		{
          // 			keyword = {'text': keyword}
          // 		}

          // 		keywords_processed.push(keyword)
          // 	}
          // 	object[key] = keywords_processed;
          // } else if(key == 'qualification_assignments_approved' || key == 'qualification_hits_approved') {
          // 	settingsBatch[key].trim() == '' ? object[key] = null : object[key] = settingsBatch[key];
          // } else if(key == 'qualification_locale') {
          // 	object[key] = JSON.stringify(settingsBatch[key]);
          // } else {
          // if(typeof(settingsBatch[key]) == 'object')
          // {
          // } else {
          // 	if(key == 'assignments_max')
          // 	{
          // 		object['count_assignments'] = settingsBatch[key];
          // 	} else if(key == 'template') {
          // 		object['fk_template_main'] = settingsBatch[key];
          // 	} else {
          // 		object[key] = settingsBatch[key];
          // 	}
          // }
          // }
          if (typeof settingsBatch[key] === 'object') {
            if (
              _.differenceBy(settingsBatch[key], this[key], (value) => value.text.toLowerCase()).length > 0
              || _.differenceBy(this[key], settingsBatch[key], (value) => value.text.toLowerCase()).length > 0
            ) {
              object[key] = settingsBatch[key];
            }
          } else {
            object[key] = settingsBatch[key];
          }
        }
      }
    }

    return object;
  }
}
