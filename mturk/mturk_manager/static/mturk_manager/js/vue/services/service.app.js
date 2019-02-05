import {store} from "../store/vuex";
import {Service_Endpoint} from "./service_endpoint";
import {Service_Projects} from "./service_projects";
console.log('1', 1);
class Class_Service_App {
    async init() {
        console.warn('init app');
        const is_success = await store.dispatch('module_app/load_credentials');

        if(is_success === false) {
            // router.push({name: 'add_credentials'});
            return false;
        }

        Service_Endpoint.init(store.state.module_app.token_instance);

        await this.load_config();

        await Service_Projects.load_projects();

        await Service_Projects.load_project_data();

    }

    async load_config() {
       const response = await Service_Endpoint.make_request({
            url: {
                path: 'config',
            },
           method: 'get',
        });
       
       console.log('config', response.data);

       await store.dispatch('module_app/init', response.data);

       return response.data
    }
}

export const Service_App = new Class_Service_App();