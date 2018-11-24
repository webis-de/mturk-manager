import {store} from "../store/vuex";
import {Service_Assignments} from "./service_assignments";

class Class_Service_HITs {
    async set_hits({object_batches, data_batches, use_sandbox})
    {
        store.commit('moduleHITs/set_hits', {
            object_batches,
            data_batches,
            use_sandbox
        });

        await Service_Assignments.set_assignments({
            object_hits: store.getters['moduleHITs/get_object_hits'](use_sandbox),
            data_batches,
            use_sandbox
        });
    }

    async append_hits({data_batches, use_sandbox})
    {
         await Service_Assignments.append_assignments({
            data_batches,
            object_hits: store.getters['moduleHITs/get_object_hits'](use_sandbox),
            use_sandbox,
        });
    }
}

export const Service_HITs = new Class_Service_HITs();