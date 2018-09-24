export default class Settings_Batch 
{
	constructor(data=undefined) 
	{
		this.id = data != undefined ? data.id : undefined;
		this.name = data != undefined ? data.name : undefined;

        this.title = data != undefined ? data.title : undefined;
        this.description = data != undefined ? data.description : undefined;
        this.keywords = data != undefined ? data.keywords : [];
        this.count_assignments = data != undefined ? data.count_assignments : undefined;
        this.reward = data != undefined ? data.reward : undefined;
        this.lifetime = data != undefined ? data.lifetime : undefined;
        this.duration = data != undefined ? data.duration : undefined;
        this.has_content_adult = data != undefined ? data.has_content_adult : false;
        this.qualification_assignments_approved = data != undefined ? data.qualification_assignments_approved : undefined;
        this.qualification_hits_approved = data != undefined ? data.qualification_hits_approved : undefined;
        this.qualification_locale = data != undefined ? data.qualification_locale : [];
        this.block_workers = data != undefined ? data.block_workers : false;
        this.template = data != undefined ? data.fk_template_main : undefined;
        this.count_assignments_max_per_worker = data != undefined ? data.count_assignments_max_per_worker : undefined;
	}

	// get_changes(project) {
	// 	const object = {};
	// 	for(const key in this)
	// 	{
	// 		if(project[key] != undefined)
	// 		{
	// 			if(this[key] != project[key])
	// 			{
	// 				console.log(`Changed value: ${key}`);
	// 				if(key == 'keywords')
	// 				{
	// 					const keywords_processed = [];
	// 					for(let keyword of project[key])
	// 					{
	// 						if(typeof(keyword) == 'string')
	// 						{
	// 							keyword = {'text': keyword}
	// 						}

	// 						keywords_processed.push(keyword)
	// 					}
	// 					object[key] = keywords_processed;
	// 				} else if(key == 'qualification_assignments_approved' || key == 'qualification_hits_approved') {
	// 					project[key].trim() == '' ? object[key] = null : object[key] = project[key];
	// 				} else if(key == 'qualification_locale') {
	// 					object[key] = JSON.stringify(project[key]);
	// 				} else {
	// 					if(typeof(project[key]) == 'object')
	// 					{
	// 						object[key] = project[key];
	// 					} else {
	// 						if(key == 'assignments_max') 
	// 						{
	// 							object['count_assignments'] = project[key];
	// 						} else if(key == 'template') {
	// 							object['fk_template_main'] = project[key];
	// 						} else {
	// 							object[key] = project[key];
	// 						}
	// 					}
	// 				}
	// 			}
	// 		}
	// 	}

	// 	return object;
	// }
}