import {router} from "./service_router";
import {store} from "../store/vuex";
import localforage from "localforage";
import {Service_Endpoint} from "./service_endpoint";
import {Service_Projects} from "./service_projects";

class Class_Service_App {
    async init() {
        console.warn('init app');
        const is_success = await store.dispatch('module_app/load_credentials');

        if(is_success === false) {
            // router.push({name: 'add_credentials'});
            return false;
        }

        Service_Endpoint.init(store.state['module_app'].token_instance);

        await this.load_config();

        await Service_Projects.load_projects();

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

//go to add_credentials if there are no credentials stored and the target route is not already add_credentials
router.beforeEach(async (to, from, next) => {
    if (store.getters['module_app/has_credentials'] === false && to.name !== 'add_credentials') {
        const is_success = await Service_App.init();
        if(is_success === false) {
            next({name: 'add_credentials'});
            return;
        }
    }

    // console.log('to', to);
    // console.log('from', from);
    next();
});
