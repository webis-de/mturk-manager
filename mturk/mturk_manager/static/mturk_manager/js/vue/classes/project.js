export default class Project 
{
	constructor(data={}) 
	{
		// console.log(data)
		this.id = data.id;
		this.name = data.name;
		this.slug = data.slug;
		this.version = data.version;
		this.settings_batch_default = data.settings_batch_default;
		this.datetime_visited = new Date(data.datetime_visited);
		this.count_assignments_max_per_worker = data.count_assignments_max_per_worker;
		
        this.templates_worker = null;
        this.templates_assignment = null;
        this.templates_hit = null;
        this.templates_global = null;
		this.settings_batch = null;

		this.message_reject_default = data.message_reject_default;

		this.sum_costs_max_sandbox = undefined;
		this.max_costs_max_sandbox = undefined;
		this.min_costs_max_sandbox = undefined;

		this.sum_costs_so_far_sandbox = undefined;
		this.max_costs_so_far_sandbox = undefined;
		this.min_costs_so_far_sandbox = undefined;

		this.sum_costs_max = undefined;
		this.max_costs_max = undefined;
		this.min_costs_max = undefined;

		this.sum_costs_so_far = undefined;
		this.max_costs_so_far = undefined;
		this.min_costs_so_far = undefined;
        // this.title = data.title;
        // this.description = data.description;
        // this.keywords = data.keywords;
        // this.assignments_max = data.count_assignments;
        // this.reward = data.reward;
        // this.lifetime = data.lifetime;
        // this.duration = data.duration;
        // this.use_sandbox = data.use_sandbox;
        // this.has_content_adult = data.has_content_adult;
        // this.qualification_assignments_approved = data.qualification_assignments_approved;
        // this.qualification_hits_approved = data.qualification_hits_approved;
        // this.qualification_locale = data.qualification_locale;
        // this.block_workers = data.block_workers;
        // this.templates = data.templates;
        // this.template = data.fk_template_main;
        // this.count_assignments_max_per_worker = data.count_assignments_max_per_worker;
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