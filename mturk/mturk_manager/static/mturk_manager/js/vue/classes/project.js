export class Project 
{
	constructor(data) 
	{
		this.id = data.id;
		this.name = data.name;
		this.slug = data.slug;
        this.title = data.title;
        this.description = data.description;
        this.keywords = data.keywords;
        this.assignments_max = data.count_assignments;
        this.reward = data.reward;
        this.lifetime = data.lifetime;
        this.duration = data.duration;
        this.use_sandbox = data.use_sandbox;
        this.has_content_adult = data.has_content_adult;
        this.qualification_assignments_approved = data.qualification_assignments_approved;
        this.qualification_hits_approved = data.qualification_hits_approved;
        this.qualification_locale = data.qualification_locale;
        this.block_workers = data.block_workers;
	}
}