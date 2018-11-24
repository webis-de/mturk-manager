import {store} from "../store/vuex";
import {Service_Templates_Assignment} from "./service_templates_assignment";
import {Service_Templates_HIT} from "./service_templates_hit";
import {Service_Templates_Global} from "./service_templates_global";
import {Service_Templates_Worker} from "./service_templates_worker";

class Class_Service_Templates {
    async load(project=store.getters['moduleProjects/get_project_current'])
    {
        await Service_Templates_Assignment.load(project);
		await Service_Templates_HIT.load(project);
		await Service_Templates_Global.load(project);
		await Service_Templates_Worker.load(project);
    }
}

export const Service_Templates = new Class_Service_Templates();