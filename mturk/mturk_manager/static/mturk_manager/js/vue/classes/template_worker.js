export default class Template_Worker 
{
	constructor(data=undefined) 
	{
		this.id = data != undefined ? data.id : undefined;
		this.name = data != undefined ? data.name : undefined;
		this.height_frame = data != undefined ? data.height_frame : 800;
		this.template = data != undefined ? data.template : undefined;
		this.dict_parameters = data != undefined ? JSON.parse(data.json_dict_parameters) : undefined;
		this.count_parameters = Object.keys(this.dict_parameters).length;
	}
}